"""
JARVIS - Backend Flask con Claude Haiku + PostgreSQL
Sistema BI conversacional para agencia de medios (Paraguay)
Incluye: Chat histórico, usuarios, roles (normal/trainer), y 10+ tipos de queries
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import json
from anthropic import Anthropic

# SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text

# Base de datos
from db import engine
from claude_handler import ClaudeHandler

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY no está configurado en .env")
    logger.info("Configuración cargada")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# SQLAlchemy
Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    query = Column(Text)
    response = Column(Text)
    query_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(255))
    role = Column(String(20), default='normal')
    created_at = Column(DateTime, default=datetime.now)

class TrainingFeedback(Base):
    __tablename__ = 'training_feedback'
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer)
    original_response = Column(Text)
    corrected_response = Column(Text)
    trainer_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

# Crear tablas
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Claude handler
claude = ClaudeHandler(os.getenv('ANTHROPIC_API_KEY'))

# ==================== FUNCIONES AUXILIARES ====================

def get_session():
    return Session()

def escape_html(text):
    """Escapa HTML"""
    if not text:
        return ""
    text = str(text)
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#039;')

# ==================== QUERIES A LA BD ====================

def get_top_clientes_enriched(query):
    """Top 5 clientes por facturación"""
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion,
                    (SUM(f.facturacion) / (SELECT SUM(facturacion) FROM fact_facturacion) * 100)::float as market_share,
                    COUNT(DISTINCT f.anio || '-' || f.mes) as meses_activo,
                    MAX(f.anio) as ultimo_año,
                    MIN(f.anio) as primer_año
                FROM dim_anunciante d
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                GROUP BY d.anunciante_id, d.nombre_canonico
                ORDER BY facturacion DESC
                LIMIT 5
            """)
            rows = conn.execute(stmt).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "cliente": r[0],
                    "facturacion": float(r[1]) if r[1] else 0,
                    "market_share": float(r[2]) if r[2] else 0,
                    "meses_activo": r[3],
                    "ultimo_año": r[4],
                    "primer_año": r[5]
                })
            return result
    except Exception as e:
        logger.error(f"Error Top Clientes: {e}")
        return []

def get_facturacion_enriched(query):
    """Facturación de un cliente específico"""
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '')
    palabras = query_limpio.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    
    if not cliente:
        return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion,
                    AVG(f.facturacion)::float as promedio_mensual,
                    (SUM(f.facturacion) / (SELECT SUM(facturacion) FROM fact_facturacion) * 100)::float as market_share
                FROM dim_anunciante d
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "cliente": r[0],
                    "facturacion": float(r[1]) if r[1] else 0,
                    "promedio_mensual": float(r[2]) if r[2] else 0,
                    "market_share": float(r[3]) if r[3] else 0
                })
            return result
    except Exception as e:
        logger.error(f"Error Facturación: {e}")
        return []

def get_comparacion_enriched(query):
    """Comparación entre 2 clientes"""
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '')
    if "vs" not in query_limpio and "versus" not in query_limpio:
        return []
    
    clientes = [c.strip() for c in query_limpio.upper().split("VS")]
    if len(clientes) != 2:
        return []
    
    try:
        with engine.connect() as conn:
            result = []
            for cliente in clientes:
                cliente = cliente.strip()
                stmt = text("""
                    SELECT 
                        d.nombre_canonico,
                        SUM(f.facturacion)::float as facturacion,
                        COUNT(DISTINCT f.anio || '-' || f.mes) as meses_activo
                    FROM dim_anunciante d
                    LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                    WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                    GROUP BY d.anunciante_id, d.nombre_canonico
                """)
                rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
                if rows:
                    r = rows[0]
                    result.append({
                        "cliente": r[0],
                        "facturacion": float(r[1]) if r[1] else 0,
                        "meses_activo": r[2]
                    })
            
            # Agregar diferencia si hay 2 resultados
            if len(result) == 2:
                diff = result[0]["facturacion"] - result[1]["facturacion"]
                diff_pct = (diff / result[1]["facturacion"] * 100) if result[1]["facturacion"] > 0 else 0
                result.append({
                    "diferencia": diff,
                    "diferencia_pct": diff_pct
                })
            
            return result
    except Exception as e:
        logger.error(f"Error Comparación: {e}")
        return []

def get_datos_cruzados_enriched(query):
    """Perfil completo con datos AdLens"""
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '')
    palabras = query_limpio.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    
    if not cliente:
        return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion_total,
                    COUNT(DISTINCT f.anio || '-' || f.mes) as meses_activo,
                    MAX(f.anio) as ultimo_año,
                    AVG(f.facturacion)::float as promedio_mensual,
                    p.rubro_principal,
                    p.cluster,
                    p.competitividad,
                    p.estructura,
                    p.ejecucion,
                    p.cultura,
                    p.inversion,
                    p.inversion_en_tv_abierta_2024_en_miles_usd,
                    p.en_que_medios_invierte_la_empresa_principalmente,
                    p.la_empresa_invierte_en_marketing_digital
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id,
                         p.rubro_principal, p.cluster, p.competitividad, p.estructura,
                         p.ejecucion, p.cultura, p.inversion,
                         p.inversion_en_tv_abierta_2024_en_miles_usd,
                         p.en_que_medios_invierte_la_empresa_principalmente,
                         p.la_empresa_invierte_en_marketing_digital
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "cliente": r[0],
                    "facturacion_total": float(r[1]) if r[1] else 0,
                    "meses_activo": r[2],
                    "ultimo_año": r[3],
                    "promedio_mensual": float(r[4]) if r[4] else 0,
                    "rubro": r[5],
                    "cluster": r[6],
                    "competitividad": r[7],
                    "estructura": r[8],
                    "ejecucion": r[9],
                    "cultura": r[10],
                    "inversion_score": r[11],
                    "inversion_tv": r[12],
                    "medios": r[13],
                    "invierte_digital": r[14]
                })
            return result
    except Exception as e:
        logger.error(f"Error Datos Cruzados: {e}")
        return []

def get_tendencia_enriched(query):
    """Tendencia de facturación anual"""
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '')
    palabras = query_limpio.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    
    if not cliente:
        return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    f.anio,
                    SUM(f.facturacion)::float as facturacion
                FROM fact_facturacion f
                JOIN dim_anunciante d ON d.anunciante_id = f.anunciante_id
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente) AND f.facturacion > 0
                GROUP BY f.anio
                ORDER BY f.anio DESC
                LIMIT 5
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "año": r[0],
                    "facturacion": float(r[1]) if r[1] else 0
                })
            
            if len(result) >= 2:
                first = result[-1]["facturacion"]
                last = result[0]["facturacion"]
                if first > 0:
                    crecimiento = ((last - first) / first * 100)
                    result.append({"crecimiento_pct": crecimiento})
            
            return result
    except Exception as e:
        logger.error(f"Error Tendencia: {e}")
        return []

def get_analisis_completo(query):
    """Análisis multi-tema cruzado"""
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '')
    palabras = query_limpio.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    
    if not cliente:
        return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion_total,
                    AVG(f.facturacion)::float as promedio_mensual,
                    p.cluster,
                    p.inversion_en_tv_abierta_2024_en_miles_usd::float as inv_tv,
                    p.inversion_en_cable_2024_en_miles_usd::float as inv_cable,
                    p.inversion_en_radio_2024_en_miles_usd::float as inv_radio,
                    p.inversion_en_pdv_2024_en_miles_usd::float as inv_pdv,
                    p.la_empresa_invierte_en_marketing_digital,
                    p.competitividad,
                    MAX(f.anio) as ultimo_año
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id, p.cluster,
                         p.inversion_en_tv_abierta_2024_en_miles_usd,
                         p.inversion_en_cable_2024_en_miles_usd,
                         p.inversion_en_radio_2024_en_miles_usd,
                         p.inversion_en_pdv_2024_en_miles_usd,
                         p.la_empresa_invierte_en_marketing_digital,
                         p.competitividad
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            
            result = []
            for r in rows:
                facturacion_2025 = float(r[1]) if r[1] else 0
                proyeccion_2026 = facturacion_2025 * 1.15
                
                result.append({
                    "cliente": r[0],
                    "facturacion_2025": facturacion_2025,
                    "promedio_mensual": float(r[2]) if r[2] else 0,
                    "cluster": r[3],
                    "inversion_tv": float(r[4]) if r[4] else 0,
                    "inversion_cable": float(r[5]) if r[5] else 0,
                    "inversion_radio": float(r[6]) if r[6] else 0,
                    "inversion_pdv": float(r[7]) if r[7] else 0,
                    "invierte_digital": r[8],
                    "competitividad": r[9],
                    "ultimo_año": r[10],
                    "proyeccion_2026": proyeccion_2026
                })
            
            return result
    except Exception as e:
        logger.error(f"Error Análisis Completo: {e}")
        return []

def get_clientes_por_cluster(query):
    """Clientes de un cluster específico"""
    import re
    query_limpio = query.lower()
    match = re.search(r'cluster\s+(\d+)', query_limpio)
    cluster_num = match.group(1) if match else None
    
    if not cluster_num:
        return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    p.cluster,
                    SUM(f.facturacion)::float as facturacion_total,
                    p.inversion_en_tv_abierta_2024_en_miles_usd::float as inv_tv,
                    p.competitividad,
                    COUNT(DISTINCT f.anio) as anos_activo
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE p.cluster::text = :cluster
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id, p.cluster,
                         p.inversion_en_tv_abierta_2024_en_miles_usd, p.competitividad
                ORDER BY facturacion_total ASC
            """)
            rows = conn.execute(stmt, {"cluster": cluster_num}).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "cliente": r[0],
                    "cluster": r[1],
                    "facturacion_total": float(r[2]) if r[2] else 0,
                    "inversion_tv": float(r[3]) if r[3] else 0,
                    "competitividad": r[4],
                    "anos_activo": r[5]
                })
            return result
    except Exception as e:
        logger.error(f"Error Clientes por Cluster: {e}")
        return []

def get_clientes_por_decision_marketing(query):
    """Clientes segmentados por decisión de marketing"""
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    CASE 
                        WHEN p.el_departamento_de_marketing_toma_decisiones_auton ILIKE 'SI%' 
                            THEN 'Dpto Marketing Autónomo'
                        ELSE 'Dueño/Gerente General'
                    END as tipo_decision,
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion_total,
                    AVG(f.facturacion)::float as promedio_mensual,
                    p.competitividad,
                    p.la_empresa_invierte_en_marketing_digital
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE p.el_departamento_de_marketing_toma_decisiones_auton IS NOT NULL
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id,
                         p.el_departamento_de_marketing_toma_decisiones_auton,
                         p.competitividad, p.la_empresa_invierte_en_marketing_digital
                ORDER BY tipo_decision, facturacion_total DESC
            """)
            rows = conn.execute(stmt).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "tipo_decision": r[0],
                    "cliente": r[1],
                    "facturacion_total": float(r[2]) if r[2] else 0,
                    "promedio_mensual": float(r[3]) if r[3] else 0,
                    "competitividad": r[4],
                    "invierte_digital": r[5]
                })
            return result
    except Exception as e:
        logger.error(f"Error Decisiones Marketing: {e}")
        return []

def get_clientes_por_nivel_confianza(query):
    """Clientes segmentados por nivel de confianza"""
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    p.que_tan_desconfiada_es_la_empresa_cuanto_cuesta_ve as nivel_confianza,
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion_total,
                    AVG(f.facturacion)::float as promedio_mensual,
                    p.competitividad
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE p.que_tan_desconfiada_es_la_empresa_cuanto_cuesta_ve IS NOT NULL
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id,
                         p.que_tan_desconfiada_es_la_empresa_cuanto_cuesta_ve,
                         p.competitividad
                ORDER BY nivel_confianza, facturacion_total DESC
            """)
            rows = conn.execute(stmt).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "nivel_confianza": r[0],
                    "cliente": r[1],
                    "facturacion_total": float(r[2]) if r[2] else 0,
                    "promedio_mensual": float(r[3]) if r[3] else 0,
                    "competitividad": r[4]
                })
            return result
    except Exception as e:
        logger.error(f"Error Nivel Confianza: {e}")
        return []

def get_facturacion_por_arena_e_inversion_digital(query):
    """Facturación en arena DISTRIBUCION DE CONTENIDO - ON"""
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    f.arena,
                    f.subarenas,
                    SUM(f.facturacion)::float as facturacion_total,
                    AVG(f.facturacion)::float as promedio,
                    p.la_empresa_invierte_en_digital::int as score_digital,
                    p.rango_de_inversion,
                    COUNT(DISTINCT f.anio) as anos_activo
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(f.arena) = 'DISTRIBUCION DE CONTENIDO'
                  AND UPPER(f.subarenas) = 'ON'
                  AND p.la_empresa_invierte_en_digital::int >= 5
                GROUP BY d.anunciante_id, d.nombre_canonico, f.arena, f.subarenas, 
                         p.id, p.la_empresa_invierte_en_digital, p.rango_de_inversion
                ORDER BY facturacion_total DESC
            """)
            rows = conn.execute(stmt).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "cliente": r[0],
                    "arena": r[1],
                    "subarena": r[2],
                    "facturacion_total": float(r[3]) if r[3] else 0,
                    "promedio_mensual": float(r[4]) if r[4] else 0,
                    "score_inversion_digital": r[5],
                    "rango_inversion": r[6],
                    "anos_activo": r[7]
                })
            return result
    except Exception as e:
        logger.error(f"Error Facturación por Arena: {e}")
        return []

def get_desconfiados_con_inversion_alta(query):
    """Clientes muy desconfiados pero con inversión alta"""
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    p.que_tan_desconfiada_es_la_empresa_cuanto_cuesta_ve as nivel_confianza,
                    SUM(f.facturacion)::float as facturacion_total,
                    p.inversion_en_tv_abierta_2024_en_miles_usd::float as inv_tv,
                    p.inversion_en_cable_2024_en_miles_usd::float as inv_cable,
                    p.inversion_en_radio_2024_en_miles_usd::float as inv_radio,
                    p.inversion_en_pdv_2024_en_miles_usd::float as inv_pdv,
                    (p.inversion_en_tv_abierta_2024_en_miles_usd::float + 
                     p.inversion_en_cable_2024_en_miles_usd::float +
                     p.inversion_en_radio_2024_en_miles_usd::float +
                     p.inversion_en_pdv_2024_en_miles_usd::float) as inversion_total,
                    p.competitividad
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE p.que_tan_desconfiada_es_la_empresa_cuanto_cuesta_ve ILIKE '%Muy desconfiada%'
                  AND ((p.inversion_en_tv_abierta_2024_en_miles_usd::float + 
                        p.inversion_en_cable_2024_en_miles_usd::float +
                        p.inversion_en_radio_2024_en_miles_usd::float +
                        p.inversion_en_pdv_2024_en_miles_usd::float) > 100)
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id,
                         p.que_tan_desconfiada_es_la_empresa_cuanto_cuesta_ve,
                         p.inversion_en_tv_abierta_2024_en_miles_usd,
                         p.inversion_en_cable_2024_en_miles_usd,
                         p.inversion_en_radio_2024_en_miles_usd,
                         p.inversion_en_pdv_2024_en_miles_usd,
                         p.competitividad
                ORDER BY inversion_total DESC
            """)
            rows = conn.execute(stmt).fetchall()
            
            result = []
            for r in rows:
                inv_total = (float(r[7]) if r[7] else 0)
                result.append({
                    "cliente": r[0],
                    "nivel_confianza": r[1],
                    "facturacion_total": float(r[2]) if r[2] else 0,
                    "inversion_tv": float(r[3]) if r[3] else 0,
                    "inversion_cable": float(r[4]) if r[4] else 0,
                    "inversion_radio": float(r[5]) if r[5] else 0,
                    "inversion_pdv": float(r[6]) if r[6] else 0,
                    "inversion_total": inv_total,
                    "competitividad": r[8]
                })
            return result
    except Exception as e:
        logger.error(f"Error Desconfiados con Inversión: {e}")
        return []

def get_analisis_cliente_especifico(query):
    """Análisis ON vs OFF de un cliente"""
    query_limpio = query.lower()
    palabras = query_limpio.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    
    if not cliente:
        if "superseis" in query_limpio:
            cliente = "SUPERSEIS"
        elif "pechugon" in query_limpio or "la blanca" in query_limpio:
            cliente = "PECHUGON"
        else:
            return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    f.arena,
                    f.subarenas,
                    SUM(f.facturacion)::float as facturacion_arena,
                    COUNT(DISTINCT f.anio || '-' || f.mes) as meses_activo,
                    p.cluster,
                    p.competitividad,
                    p.la_empresa_invierte_en_digital
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico, f.arena, f.subarenas, 
                         p.id, p.cluster, p.competitividad, p.la_empresa_invierte_en_digital
                ORDER BY facturacion_arena DESC
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            
            result = []
            total_facturacion = 0
            on_facturacion = 0
            
            for r in rows:
                facturacion = float(r[3]) if r[3] else 0
                total_facturacion += facturacion
                
                is_on = "ON" in (r[2] or "").upper() or "DIGITAL" in (r[1] or "").upper()
                if is_on:
                    on_facturacion += facturacion
                
                result.append({
                    "cliente": r[0],
                    "arena": r[1],
                    "subarena": r[2],
                    "facturacion": facturacion,
                    "meses_activo": r[4],
                    "cluster": r[5],
                    "competitividad": r[6],
                    "invierte_digital": r[7],
                    "es_on": is_on
                })
            
            if result:
                result.append({
                    "resumen": True,
                    "total_facturacion": total_facturacion,
                    "on_facturacion": on_facturacion,
                    "off_facturacion": total_facturacion - on_facturacion,
                    "porcentaje_on": (on_facturacion / total_facturacion * 100) if total_facturacion > 0 else 0
                })
            
            return result
    except Exception as e:
        logger.error(f"Error Análisis Cliente Específico: {e}")
        return []

def get_clientes_por_atributo_adlens_arena(query):
    """Clientes con atributo AdLens en una arena"""
    query_limpio = query.lower()
    
    cliente_buscar = None
    if "puma" in query_limpio:
        cliente_buscar = "PUMA"
    
    atributo = None
    if "valiente" in query_limpio or "arriesgada" in query_limpio:
        atributo = "Innovadora y valiente"
    elif "conservadora" in query_limpio:
        atributo = "Muy conservadora"
    elif "discreta" in query_limpio:
        atributo = "Discreta"
    
    arenas_buscar = []
    if "creatividad" in query_limpio:
        arenas_buscar = ["CREACION DE CONTENIDO", "CREATIVIDAD"]
    elif "contenido" in query_limpio or "on" in query_limpio or "off" in query_limpio:
        arenas_buscar = ["DISTRIBUCION DE CONTENIDO", "CREACION DE CONTENIDO"]
    elif "creacion" in query_limpio:
        arenas_buscar = ["CREACION DE CONTENIDO"]
    
    if not (atributo or cliente_buscar) or not arenas_buscar:
        return []
    
    try:
        with engine.connect() as conn:
            if cliente_buscar:
                stmt = text("""
                    SELECT 
                        d.nombre_canonico,
                        p.con_respecto_al_marketing_y_la_publicidad_es_una_e as atributo,
                        f.arena,
                        f.subarenas,
                        SUM(f.facturacion)::float as facturacion_total,
                        AVG(f.facturacion)::float as promedio_mensual,
                        p.inversion_en_tv_abierta_2024_en_miles_usd::float as inv_tv,
                        p.la_marca_empresa_se_destaca_por_innovar_en_publici as innova_score,
                        p.competitividad
                    FROM dim_anunciante d
                    LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                    LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                    WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                      AND UPPER(f.arena) IN ('CREACION DE CONTENIDO', 'DISTRIBUCION DE CONTENIDO', 'CREATIVIDAD')
                    GROUP BY d.anunciante_id, d.nombre_canonico, p.id,
                             p.con_respecto_al_marketing_y_la_publicidad_es_una_e,
                             f.arena, f.subarenas,
                             p.inversion_en_tv_abierta_2024_en_miles_usd,
                             p.la_marca_empresa_se_destaca_por_innovar_en_publici,
                             p.competitividad
                    ORDER BY f.arena, facturacion_total DESC
                """)
                rows = conn.execute(stmt, {"cliente": f"%{cliente_buscar}%"}).fetchall()
            else:
                stmt = text("""
                    SELECT 
                        d.nombre_canonico,
                        p.con_respecto_al_marketing_y_la_publicidad_es_una_e as atributo,
                        f.arena,
                        f.subarenas,
                        SUM(f.facturacion)::float as facturacion_total,
                        AVG(f.facturacion)::float as promedio_mensual,
                        p.inversion_en_tv_abierta_2024_en_miles_usd::float as inv_tv,
                        p.la_marca_empresa_se_destaca_por_innovar_en_publici as innova_score,
                        p.competitividad
                    FROM dim_anunciante d
                    LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                    LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                    WHERE p.con_respecto_al_marketing_y_la_publicidad_es_una_e ILIKE :atributo
                      AND UPPER(f.arena) IN ('CREACION DE CONTENIDO', 'DISTRIBUCION DE CONTENIDO', 'CREATIVIDAD')
                    GROUP BY d.anunciante_id, d.nombre_canonico, p.id,
                             p.con_respecto_al_marketing_y_la_publicidad_es_una_e,
                             f.arena, f.subarenas,
                             p.inversion_en_tv_abierta_2024_en_miles_usd,
                             p.la_marca_empresa_se_destaca_por_innovar_en_publici,
                             p.competitividad
                    ORDER BY f.arena, facturacion_total DESC
                """)
                rows = conn.execute(stmt, {"atributo": f"%{atributo}%"}).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "cliente": r[0],
                    "atributo": r[1],
                    "arena": r[2],
                    "subarena": r[3],
                    "facturacion_total": float(r[4]) if r[4] else 0,
                    "promedio_mensual": float(r[5]) if r[5] else 0,
                    "inversion_tv": float(r[6]) if r[6] else 0,
                    "innova_score": r[7],
                    "competitividad": r[8]
                })
            return result
    except Exception as e:
        logger.error(f"Error Atributo AdLens + Arena: {e}")
        return []

# ==================== ENDPOINTS ====================

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Obtener historial de chat del usuario"""
    try:
        session = get_session()
        user_id = request.args.get('user_id', 1, type=int)
        
        conversations = session.query(Conversation)\
            .filter_by(user_id=user_id)\
            .order_by(Conversation.created_at.desc())\
            .limit(50)\
            .all()
        
        result = [{
            "id": c.id,
            "query": c.query,
            "response": c.response,
            "query_type": c.query_type,
            "created_at": c.created_at.isoformat()
        } for c in conversations]
        
        session.close()
        return jsonify({"success": True, "conversations": result}), 200
    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        return jsonify({"error": str(e)}), 500

def mock_claude_response(query_type, rows, user_query):
    """Respuestas hardcodeadas para demo (sin gastar API)"""
    
    if query_type == "ranking":
        return "Top 5 clientes: CERVEPAR (29.6B), TELEFONICA (12B), GENERAL MOTORS (11.5B), UNILEVER (9B), BANCO FAMILIAR (6.4B). Estos concentran el 60% de la facturación total."
    
    elif query_type == "facturacion":
        if rows:
            cliente = rows[0].get("cliente", "Cliente")
            facturacion = rows[0].get("facturacion", 0)
            market_share = rows[0].get("market_share", 0)
            return f"{cliente} facturó {facturacion:,.0f} Gs (market share: {market_share:.2f}%)."
        return "No tengo datos de facturación para ese cliente."
    
    elif query_type == "analisis_completo":
        if rows:
            r = rows[0]
            return f"{r.get('cliente')}: Facturación 2025: {r.get('facturacion_2025', 0):,.0f} Gs. Inversión TV: {r.get('inversion_tv', 0):.2f}K USD. Proyección 2026: {r.get('proyeccion_2026', 0):,.0f} Gs (+15% estimado)."
        return "No hay datos disponibles para ese análisis."
    
    elif query_type == "comparacion":
        if len(rows) >= 2:
            return f"{rows[0]['cliente']} facturó {rows[0]['facturacion']:,.0f} Gs vs {rows[1]['cliente']} con {rows[1]['facturacion']:,.0f} Gs."
        return "No puedo comparar sin dos clientes."
    
    elif query_type == "clientes_cluster":
        if rows:
            return f"Cluster {rows[0]['cluster']}: {len(rows)} clientes encontrados. El de menor facturación es {rows[0]['cliente']} con {rows[0]['facturacion_total']:,.0f} Gs."
        return "No hay clientes en ese cluster."
    
    elif query_type == "decision_marketing":
        dpto = sum(1 for r in rows if r.get('tipo_decision') == 'Dpto Marketing Autónomo')
        dueno = sum(1 for r in rows if r.get('tipo_decision') == 'Dueño/Gerente General')
        return f"Empresas con Dpto Marketing: {dpto}. Con Dueño decidiendo: {dueno}. Los que tienen departamento facturan más en promedio."
    
    elif query_type == "nivel_confianza":
        muy_desconfiados = [r for r in rows if "Muy desconfiada" in str(r.get('nivel_confianza', ''))]
        return f"Hay {len(muy_desconfiados)} clientes 'muy desconfiados'. El más facturador es {muy_desconfiados[0]['cliente'] if muy_desconfiados else 'N/A'} con {muy_desconfiados[0].get('facturacion_total', 0):,.0f} Gs si existe."
    
    elif query_type == "arena_digital":
        if rows:
            total = sum(r.get('facturacion_total', 0) for r in rows)
            return f"En DISTRIBUCION DE CONTENIDO - ON, empresas que invierten en digital facturan {total:,.0f} Gs en total. Top: {rows[0]['cliente']} con {rows[0]['facturacion_total']:,.0f} Gs."
        return "No hay datos en esa arena."
    
    elif query_type == "atributo_adlens_arena":
        if rows:
            return f"{rows[0]['cliente']}: Posicionada como '{rows[0]['atributo']}'. En {rows[0]['arena']}: {rows[0]['facturacion_total']:,.0f} Gs facturados."
        return "No hay datos para ese atributo y arena."
    
    else:
        return f"[DEBUG] Query type: {query_type}. Registros encontrados: {len(rows)}."

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query', '').strip()
    user_id = data.get('user_id', 1)
    
    if not user_query:
        return jsonify({"error": "Query vacío"}), 400
    
    try:
        query_lower = user_query.lower()
        rows = []
        query_type = "generico"
        
        # ORDEN IMPORTA: Lo más específico primero
        
        # 1. Análisis inversión vs facturación
        if any(w in query_lower for w in ["porcentaje", "representa", "ratio", "roi"]) and \
           any(w in query_lower for w in ["inversion", "inversión", "facturacion", "facturación"]):
            query_type = "inversion_vs_facturacion"
            rows = get_analisis_inversion_vs_facturacion(user_query)
            logger.info(f"🔍 Detectado: inversion_vs_facturacion - rows: {len(rows)}")
        
        # 2. Atributo AdLens + Arena
        elif (any(w in query_lower for w in ["valiente", "conservadora", "discreta", "arriesgada", "innovadora"]) or \
              any(w in query_lower for w in ["puma energy", "puma"])) and \
             any(w in query_lower for w in ["creatividad", "contenido", "arena", "laburos", "trabajos"]):
            query_type = "atributo_adlens_arena"
            rows = get_clientes_por_atributo_adlens_arena(user_query)
            logger.info(f"🔍 Detectado: atributo_adlens_arena - rows: {len(rows)}")
        
        # 3. Cliente específico ON/OFF
        elif any(w in query_lower for w in ["superseis", "pechugon", "la blanca", "retail"]) or \
             (any(c.isupper() for c in user_query.split()[0] if user_query.split()) and \
              any(w in query_lower for w in ["on", "off", "digital", "mix", "desglose", "porcentaje"])):
            query_type = "cliente_especifico"
            rows = get_analisis_cliente_especifico(user_query)
            logger.info(f"🔍 Detectado: cliente_especifico - rows: {len(rows)}")
        
        # 4. Desconfiados con inversión
        elif any(w in query_lower for w in ["desconfiado", "confianza"]) and \
             any(w in query_lower for w in ["inversion", "inversión", "afuera", "gastan"]):
            query_type = "desconfiados_con_inversion"
            rows = get_desconfiados_con_inversion_alta(user_query)
            logger.info(f"🔍 Detectado: desconfiados_con_inversion - rows: {len(rows)}")
        
        # 5. Arena digital
        elif any(w in query_lower for w in ["arena", "distribucion"]) and \
             any(w in query_lower for w in ["digital", "invierte"]):
            query_type = "arena_digital"
            rows = get_facturacion_por_arena_e_inversion_digital(user_query)
            logger.info(f"🔍 Detectado: arena_digital - rows: {len(rows)}")
        
        # 6. Clientes por cluster
        elif "cluster" in query_lower and any(c.isdigit() for c in user_query):
            query_type = "clientes_cluster"
            rows = get_clientes_por_cluster(user_query)
            logger.info(f"🔍 Detectado: clientes_cluster - rows: {len(rows)}")
        
        # 7. Decisión de marketing
        elif any(w in query_lower for w in ["departamento", "dpto", "dueño", "gerente", "decision", "decisión"]) and \
             "marketing" in query_lower:
            query_type = "decision_marketing"
            rows = get_clientes_por_decision_marketing(user_query)
            logger.info(f"🔍 Detectado: decision_marketing - rows: {len(rows)}")
        
        # 8. Nivel de confianza
        elif any(w in query_lower for w in ["desconfiado", "confianza", "convencer"]):
            query_type = "nivel_confianza"
            rows = get_clientes_por_nivel_confianza(user_query)
            logger.info(f"🔍 Detectado: nivel_confianza - rows: {len(rows)}")
        
        # 9. Análisis completo multi-tema
        elif sum([
            "cuanto" in query_lower or "cuánto" in query_lower,
            "facturo" in query_lower or "facturación" in query_lower,
            "inversion" in query_lower or "inversión" in query_lower,
            "cluster" in query_lower,
            "2026" in query_lower or "proyección" in query_lower,
            "digital" in query_lower,
            "tv" in query_lower
        ]) >= 2:
            query_type = "analisis_completo"
            rows = get_analisis_completo(user_query)
            logger.info(f"🔍 Detectado: analisis_completo - rows: {len(rows)}")
        
        # 10. Top clientes
        elif any(w in query_lower for w in ["top", "ranking", "principal", "importante", "mayor", "más"]):
            query_type = "ranking"
            rows = get_top_clientes_enriched(user_query)
            logger.info(f"🔍 Detectado: ranking - rows: {len(rows)}")
        
        # 11. Facturación simple
        elif "cuánto" in query_lower or "factur" in query_lower:
            query_type = "facturacion"
            rows = get_facturacion_enriched(user_query)
            logger.info(f"🔍 Detectado: facturacion - rows: {len(rows)}")
        
        # 12. Comparación
        elif "vs" in query_lower or "versus" in query_lower:
            query_type = "comparacion"
            rows = get_comparacion_enriched(user_query)
            logger.info(f"🔍 Detectado: comparacion - rows: {len(rows)}")
        
        # 13. Tendencia
        elif any(w in query_lower for w in ["tendencia", "crecimiento", "variación", "cambio"]):
            query_type = "tendencia"
            rows = get_tendencia_enriched(user_query)
            logger.info(f"🔍 Detectado: tendencia - rows: {len(rows)}")
        
        # 14. Perfil completo
        elif any(w in query_lower for w in ["perfil", "quién es", "como es", "empresa", "tipo", "caracteristic"]):
            query_type = "perfil_completo"
            rows = get_datos_cruzados_enriched(user_query)
            logger.info(f"🔍 Detectado: perfil_completo - rows: {len(rows)}")
        
        else:
            return jsonify({"success": False, "response": "Consulta no reconocida. Prueba: 'Top 5 clientes', 'Cuánto facturó CERVEPAR?', 'CERVEPAR vs UNILEVER'"}), 200
        
        logger.info(f"Query type: {query_type}")
        logger.info(f"Rows count: {len(rows)}")
        logger.info(f"Rows data: {json.dumps(rows[:2], default=str)}")
                
        # Claude enhances response
        # response_text = claude.enhance_response(user_query, rows, query_type)
        response_text = mock_claude_response(query_type, rows, user_query)

        # Guardar en BD
        session = get_session()
        try:
            conversation = Conversation(
                user_id=user_id,
                query=user_query,
                response=response_text,
                query_type=query_type
            )
            session.add(conversation)
            session.commit()
            conv_id = conversation.id
        except Exception as db_err:
            logger.error(f"Error guardando en BD: {db_err}")
            conv_id = None
        finally:
            session.close()
        
        return jsonify({
            "success": True,
            "response": response_text,
            "query_type": query_type,
            "rows": rows,
            "conversation_id": conv_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"status": "✅ OK", "db": "connected"}), 200
    except:
        return jsonify({"status": "❌ ERROR", "db": "disconnected"}), 500

if __name__ == '__main__':
    logger.info("🚀 JARVIS Backend iniciando...")
    app.run(host='0.0.0.0', port=5000, debug=True)