import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import engine, test_connection
from claude_handler import ClaudeHandler
from sqlalchemy import text
from datetime import datetime, timedelta
from difflib import SequenceMatcher

load_dotenv('config/.env')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
claude = ClaudeHandler(ANTHROPIC_API_KEY)

def fuzzy_match_cliente(cliente_buscado, threshold=0.6):
    """Buscar cliente por similitud de nombre"""
    try:
        with engine.connect() as conn:
            stmt = text("SELECT DISTINCT nombre_anunciante FROM dim_anunciante_perfil WHERE nombre_anunciante IS NOT NULL")
            nombres = conn.execute(stmt).fetchall()
            
            mejores_matches = []
            for nombre_row in nombres:
                nombre = nombre_row[0]
                ratio = SequenceMatcher(None, cliente_buscado.upper(), nombre.upper()).ratio()
                if ratio >= threshold:
                    mejores_matches.append((nombre, ratio))
            
            if mejores_matches:
                mejores_matches.sort(key=lambda x: x[1], reverse=True)
                return mejores_matches[0][0]
            return None
    except Exception as e:
        logger.error(f"Error fuzzy match: {e}")
        return None


@app.before_request
def check_db():
    if not hasattr(app, 'db_checked'):
        if not test_connection():
            return jsonify({"error": "BD no disponible"}), 503
        app.db_checked = True

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query', '').strip()
    
    if not user_query:
        return jsonify({"error": "Query vacío"}), 400
    
    try:
        query_lower = user_query.lower()
        
        # ORDEN IMPORTA: Lo más específico primero
        
        # 1. Análisis inversión vs facturación (porcentaje, ratio, ROI)
        if any(w in query_lower for w in ["porcentaje", "representa", "ratio", "roi"]) and \
           any(w in query_lower for w in ["inversion", "inversión", "facturacion", "facturación"]):
            query_type = "inversion_vs_facturacion"
            rows = get_analisis_inversion_vs_facturacion(user_query)
            logger.info(f"🔍 Detectado: inversion_vs_facturacion - rows: {len(rows)}")
        
        # 2. Clientes por nivel de confianza
        elif any(w in query_lower for w in ["desconfiado", "confianza", "convencer"]):
            query_type = "nivel_confianza"
            rows = get_clientes_por_nivel_confianza(user_query)
            logger.info(f"🔍 Detectado: nivel_confianza - rows: {len(rows)}")
        
        # 3. Clientes por decisión de marketing
        elif any(w in query_lower for w in ["departamento", "dpto", "dueño", "gerente", "decision", "decisión"]) and \
             "marketing" in query_lower:
            query_type = "decision_marketing"
            rows = get_clientes_por_decision_marketing(user_query)
            logger.info(f"🔍 Detectado: decision_marketing - rows: {len(rows)}")

        # Después de "decision_marketing", antes de "clientes_cluster"
        elif any(w in query_lower for w in ["arena", "distribucion"]) and \
            any(w in query_lower for w in ["digital", "invierte"]):
            query_type = "arena_digital"
            rows = get_facturacion_por_arena_e_inversion_digital(user_query)
            logger.info(f"🔍 Detectado: arena_digital - rows: {len(rows)}")
        
        # 4. Clientes por cluster
        elif "cluster" in query_lower and any(c.isdigit() for c in user_query):
            query_type = "clientes_cluster"
            rows = get_clientes_por_cluster(user_query)
            logger.info(f"🔍 Detectado: clientes_cluster - rows: {len(rows)}")
        
        # 5. Análisis completo multi-tema
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
        
        # 6. Top clientes
        elif any(w in query_lower for w in ["top", "ranking", "principal", "importante", "mayor", "más"]):
            query_type = "ranking"
            rows = get_top_clientes_enriched(user_query)
            logger.info(f"🔍 Detectado: ranking - rows: {len(rows)}")
        
        # 7. Facturación simple
        elif "cuánto" in query_lower or "factur" in query_lower:
            query_type = "facturacion"
            rows = get_facturacion_enriched(user_query)
            logger.info(f"🔍 Detectado: facturacion - rows: {len(rows)}")
        
        # 8. Comparación
        elif "vs" in query_lower or "versus" in query_lower:
            query_type = "comparacion"
            rows = get_comparacion_enriched(user_query)
            logger.info(f"🔍 Detectado: comparacion - rows: {len(rows)}")
        
        # 9. Tendencia
        elif any(w in query_lower for w in ["tendencia", "crecimiento", "variación", "cambio"]):
            query_type = "tendencia"
            rows = get_tendencia_enriched(user_query)
            logger.info(f"🔍 Detectado: tendencia - rows: {len(rows)}")
        
        # 10. Perfil completo
        elif any(w in query_lower for w in ["perfil", "quién es", "como es", "empresa", "tipo", "caracteristic"]):
            query_type = "perfil_completo"
            rows = get_datos_cruzados_enriched(user_query)
            logger.info(f"🔍 Detectado: perfil_completo - rows: {len(rows)}")
        
        else:
            return jsonify({"success": False, "response": "Consulta no reconocida. Prueba: 'Top 5 clientes', 'Cuánto facturó CERVEPAR?', 'CERVEPAR vs UNILEVER'"}), 200
        
        response_text = claude.enhance_response(user_query, rows, query_type)
        if not response_text:
            response_text = str(rows)
        
        return jsonify({"success": True, "response": response_text, "query_type": query_type, "rows": rows}), 200
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    

def get_top_clientes_enriched(query, limit=5):
    try:
        with engine.connect() as conn:
            stmt = text("""
                WITH ranking_data AS (
                    SELECT 
                        d.anunciante_id,
                        d.nombre_canonico,
                        SUM(f.facturacion)::float as total_facturacion,
                        COUNT(DISTINCT f.anio) as years_active,
                        MAX(f.anio) as last_year,
                        MIN(f.anio) as first_year
                    FROM fact_facturacion f
                    JOIN dim_anunciante d ON d.anunciante_id = f.anunciante_id
                    WHERE f.facturacion > 0
                    GROUP BY d.anunciante_id, d.nombre_canonico
                    ORDER BY total_facturacion DESC
                    LIMIT :limit
                ),
                total_market AS (
                    SELECT SUM(facturacion)::float as market_total
                    FROM fact_facturacion
                    WHERE facturacion > 0
                )
                SELECT 
                    r.nombre_canonico,
                    r.total_facturacion,
                    ROUND((r.total_facturacion / t.market_total * 100)::numeric, 2) as market_share,
                    r.years_active,
                    r.last_year,
                    r.first_year
                FROM ranking_data r, total_market t
            """)
            rows = conn.execute(stmt, {"limit": limit}).fetchall()
            return [{"cliente": r[0], "facturacion": float(r[1]), "market_share": float(r[2]), "años_activo": r[3], "ultimo_año": r[4], "primer_año": r[5]} for r in rows]
    except Exception as e:
        logger.error(f"Error Top: {e}")
        return []

def get_facturacion_enriched(query):
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
                    SUM(f.facturacion)::float as total_facturacion,
                    ROUND((SUM(f.facturacion) / (SELECT SUM(facturacion) FROM fact_facturacion WHERE facturacion > 0) * 100)::numeric, 2) as market_share,
                    AVG(f.facturacion)::float as promedio_mensual,
                    MAX(f.facturacion)::float as mes_pico,
                    MIN(f.facturacion)::float as mes_bajo,
                    COUNT(DISTINCT (f.anio::text || '-' || f.mes::text)) as meses_facturados
                FROM fact_facturacion f
                JOIN dim_anunciante d ON d.anunciante_id = f.anunciante_id
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                AND f.facturacion > 0
                GROUP BY d.anunciante_id, d.nombre_canonico
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            return [{"cliente": r[0], "facturacion": float(r[1]), "market_share": float(r[2]), "promedio_mensual": float(r[3]), "mes_pico": float(r[4]), "mes_bajo": float(r[5]), "meses_activo": r[6]} for r in rows]
    except Exception as e:
        logger.error(f"Error Facturacion: {e}")
        return []

def get_comparacion_enriched(query):
    partes = query.lower().split("vs")
    if len(partes) != 2:
        return []
    
    cliente1 = partes[0].strip().split()[-1].upper()
    cliente2 = partes[1].strip().split()[0].upper()
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as total_facturacion,
                    AVG(f.facturacion)::float as promedio_mensual,
                    COUNT(DISTINCT CONCAT(f.anio, '-', f.mes)) as meses_activo
                FROM fact_facturacion f
                JOIN dim_anunciante d ON d.anunciante_id = f.anunciante_id
                WHERE (UPPER(d.nombre_canonico) LIKE UPPER(:cliente1) OR UPPER(d.nombre_canonico) LIKE UPPER(:cliente2))
                AND f.facturacion > 0
                GROUP BY d.anunciante_id, d.nombre_canonico
                ORDER BY total_facturacion DESC
            """)
            rows = conn.execute(stmt, {"cliente1": f"%{cliente1}%", "cliente2": f"%{cliente2}%"}).fetchall()
            result = [{"cliente": r[0], "facturacion": float(r[1]), "promedio": float(r[2]), "meses": r[3]} for r in rows]
            
            if len(result) == 2:
                dif = result[0]["facturacion"] - result[1]["facturacion"]
                pct = (dif / result[1]["facturacion"] * 100) if result[1]["facturacion"] > 0 else 0
                result.append({"diferencia": float(dif), "diferencia_pct": float(pct)})
            
            return result
    except Exception as e:
        logger.error(f"Error Comparacion: {e}")
        return []

def get_perfil_enriched(query):
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
                    COUNT(DISTINCT (f.anio::text || '-' || f.mes::text)) as meses_activo,
                    MAX(f.anio) as ultimo_año,
                    AVG(f.facturacion)::float as promedio_mensual
                FROM dim_anunciante d
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            return [{"cliente": r[0], "facturacion": float(r[1]) if r[1] else 0, "meses_activo": r[2] or 0, "ultimo_año": r[3], "promedio_mensual": float(r[4]) if r[4] else 0} for r in rows]
    except Exception as e:
        logger.error(f"Error Perfil: {e}")
        return []

def get_tendencia_enriched(query):
    palabras = query.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    
    if not cliente:
        return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    f.anio,
                    SUM(f.facturacion)::float as facturacion_anual
                FROM fact_facturacion f
                JOIN dim_anunciante d ON d.anunciante_id = f.anunciante_id
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                AND f.facturacion > 0
                GROUP BY f.anio
                ORDER BY f.anio DESC
                LIMIT 5
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            result = [{"año": r[0], "facturacion": float(r[1])} for r in rows]
            
            if len(result) >= 2:
                crecimiento = ((result[0]["facturacion"] - result[-1]["facturacion"]) / result[-1]["facturacion"] * 100) if result[-1]["facturacion"] > 0 else 0
                result.append({"crecimiento_pct": float(crecimiento)})
            
            return result
    except Exception as e:
        logger.error(f"Error Tendencia: {e}")
        return []
    
def get_datos_cruzados_enriched(query):
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '')
    palabras = query_limpio.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    
    if not cliente:
        return []
    
    cliente_match = fuzzy_match_cliente(cliente)
    if not cliente_match:
        cliente_match = cliente
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    p.rubro_principal,
                    p.que_tipo_de_empresa_es,
                    p.tamano_de_la_empresa_cantidad_de_empleados,
                    p.cluster,
                    p.en_que_medios_invierte_la_empresa_principalmente,
                    p.la_empresa_invierte_en_marketing_digital,
                    p.la_empresa_tiene_un_crm,
                    p.cultura,
                    p.competitividad,
                    p.estructura,
                    p.ejecucion,
                    p.inversion,
                    SUM(f.facturacion)::float as facturacion_total,
                    AVG(f.facturacion)::float as promedio_mensual
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id, p.rubro_principal, p.que_tipo_de_empresa_es, 
                         p.tamano_de_la_empresa_cantidad_de_empleados, p.cluster, p.en_que_medios_invierte_la_empresa_principalmente,
                         p.la_empresa_invierte_en_marketing_digital, p.la_empresa_tiene_un_crm, p.cultura, p.competitividad,
                         p.estructura, p.ejecucion, p.inversion, p.id
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            return [{
                "cliente": r[0],
                "rubro": r[1],
                "tipo_empresa": r[2],
                "tamaño": r[3],
                "cluster": r[4],
                "medios": r[5],
                "digital": r[6],
                "crm": r[7],
                "cultura": r[8],
                "competitividad": r[9],
                "estructura": r[10],
                "ejecucion": r[11],
                "inversion": r[12],
                "facturacion": float(r[13]) if r[13] else 0,
                "promedio_mensual": float(r[14]) if r[14] else 0
            } for r in rows]
    except Exception as e:
        logger.error(f"Error Datos Cruzados: {e}")
        return []
    
def get_analisis_completo(query):
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '')
    palabras = query_limpio.split()
    # Buscar palabras en mayúsculas O que sea "cervepar"
    cliente = ""
    for p in palabras:
        if p.isupper() and len(p) > 2:
            cliente = p
            break
    
    # Si no encuentra mayúscula, busca "cervepar" específicamente
    if not cliente:
        if "cervepar" in query_limpio:
            cliente = "CERVEPAR"
        else:
            palabras_caps = [p.upper() for p in palabras if len(p) > 2 and not p.isdigit()]
            if palabras_caps:
                cliente = palabras_caps[0]
    
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
                    p.inversion_en_tv_abierta_2024_en_miles_usd,
                    p.inversion_en_cable_2024_en_miles_usd,
                    p.inversion_en_radio_2024_en_miles_usd,
                    p.inversion_en_pdv_2024_en_miles_usd,
                    p.en_que_medios_invierte_la_empresa_principalmente,
                    p.la_empresa_invierte_en_marketing_digital,
                    p.puntaje_total,
                    p.competitividad,
                    p.cultura,
                    p.estructura,
                    p.ejecucion,
                    p.inversion,
                    MAX(f.anio) as ultimo_año
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id, p.cluster, 
                         p.inversion_en_tv_abierta_2024_en_miles_usd, p.inversion_en_cable_2024_en_miles_usd,
                         p.inversion_en_radio_2024_en_miles_usd, p.inversion_en_pdv_2024_en_miles_usd,
                         p.en_que_medios_invierte_la_empresa_principalmente, p.la_empresa_invierte_en_marketing_digital,
                         p.puntaje_total, p.competitividad, p.cultura, p.estructura, p.ejecucion, p.inversion
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            
            result = []
            for r in rows:
                facturacion_2025 = float(r[1]) if r[1] else 0
                crecimiento_estimado = 1.15
                proyeccion_2026 = facturacion_2025 * crecimiento_estimado
                
                result.append({
                    "cliente": r[0],
                    "facturacion_2025": facturacion_2025,
                    "promedio_mensual": float(r[2]) if r[2] else 0,
                    "cluster": r[3],
                    "inversion_tv": r[4],
                    "inversion_cable": r[5],
                    "inversion_radio": r[6],
                    "inversion_pdv": r[7],
                    "medios": r[8],
                    "invierte_digital": r[9],
                    "puntaje": r[10],
                    "competitividad": r[11],
                    "cultura": r[12],
                    "estructura": r[13],
                    "ejecucion": r[14],
                    "inversion_score": r[15],
                    "ultimo_año": r[16],
                    "proyeccion_2026": proyeccion_2026
                })
            
            return result
    except Exception as e:
        logger.error(f"Error Análisis Completo: {e}")
        return []

def get_clientes_por_cluster(query):
    """Clientes de un cluster específico"""
    query_limpio = query.lower()
    
    import re
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
                    p.inversion_en_tv_abierta_2024_en_miles_usd,
                    p.competitividad,
                    COUNT(DISTINCT f.anio) as anos_activo
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id
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
    """Clientes segmentados por quién toma decisiones de marketing"""
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
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id
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
    """Clientes segmentados por nivel de desconfianza"""
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


def get_analisis_inversion_vs_facturacion(query):
    """Análisis cruzado: inversión en medios vs facturación"""
    query_limpio = query.lower()
    cliente = ""
    
    palabras = query_limpio.split()
    for p in palabras:
        if p.upper() != p.lower() and len(p) > 2:  # Detecta palabras con mayúscula
            cliente = p.upper()
            break
    
    if not cliente:
        if "banco familiar" in query_limpio:
            cliente = "BANCO FAMILIAR"
        else:
            return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion_total,
                    p.inversion_en_tv_abierta_2024_en_miles_usd::float as inv_tv,
                    p.inversion_en_cable_2024_en_miles_usd::float as inv_cable,
                    p.inversion_en_radio_2024_en_miles_usd::float as inv_radio,
                    p.inversion_en_pdv_2024_en_miles_usd::float as inv_pdv,
                    p.rango_de_inversion
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico, p.id,
                         p.inversion_en_tv_abierta_2024_en_miles_usd,
                         p.inversion_en_cable_2024_en_miles_usd,
                         p.inversion_en_radio_2024_en_miles_usd,
                         p.inversion_en_pdv_2024_en_miles_usd,
                         p.rango_de_inversion
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            
            result = []
            for r in rows:
                inv_tv = float(r[2]) if r[2] else 0
                inv_cable = float(r[3]) if r[3] else 0
                inv_radio = float(r[4]) if r[4] else 0
                inv_pdv = float(r[5]) if r[5] else 0
                inv_total = inv_tv + inv_cable + inv_radio + inv_pdv
                facturacion = float(r[1]) if r[1] else 0
                
                # Ratio: facturación / inversión (en miles)
                ratio = facturacion / (inv_total * 1000) if inv_total > 0 else 0
                
                result.append({
                    "cliente": r[0],
                    "facturacion_total": facturacion,
                    "inversion_tv": inv_tv,
                    "inversion_cable": inv_cable,
                    "inversion_radio": inv_radio,
                    "inversion_pdv": inv_pdv,
                    "inversion_total": inv_total,
                    "rango_inversion": r[6],
                    "ratio_facturacion_inversion": ratio
                })
            return result
    except Exception as e:
        logger.error(f"Error Análisis Inversión: {e}")
        return []
    
def get_facturacion_por_arena_e_inversion_digital(query):
    """Facturación en arena específica de empresas con inversión digital"""
    query_limpio = query.lower()
    
    try:
        with engine.connect() as conn:
            # Detectar si busca inversión "mucho" o "poco"
            inversion_nivel = "SI" if "mucho" in query_limpio else None
            
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    f.arena,
                    f.subarenas,
                    SUM(f.facturacion)::float as facturacion_total,
                    AVG(f.facturacion)::float as promedio,
                    p.la_empresa_invierte_en_digital,
                    p.rango_de_inversion,
                    COUNT(DISTINCT f.anio) as anos_activo
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE f.arena ILIKE '%DISTRIBUCION DE CONTENIDO%'
                  AND f.subarenas ILIKE '%ON%'
                  AND p.la_empresa_invierte_en_digital ILIKE 'SI%'
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
                    "invierte_digital": r[5],
                    "rango_inversion": r[6],
                    "anos_activo": r[7]
                })
            return result
    except Exception as e:
        logger.error(f"Error Facturación por Arena: {e}")
        return []
    

def get_facturacion_por_arena_e_inversion_digital(query):
    """Facturación en arena específica de empresas con inversión digital"""
    query_limpio = query.lower()
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    f.arena,
                    f.subarenas,
                    SUM(f.facturacion)::float as facturacion_total,
                    AVG(f.facturacion)::float as promedio,
                    p.la_empresa_invierte_en_digital,
                    p.rango_de_inversion,
                    COUNT(DISTINCT f.anio) as anos_activo
                FROM dim_anunciante d
                LEFT JOIN dim_anunciante_perfil p ON d.anunciante_id = p.anunciante_id
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(f.arena) LIKE '%DISTRIBUCION%'
                  AND (UPPER(f.subarenas) LIKE '%CONTENT%' OR UPPER(f.subarenas) LIKE '%ON%')
                  AND p.la_empresa_invierte_en_digital ILIKE 'SI%'
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
                    "invierte_digital": r[5],
                    "rango_inversion": r[6],
                    "anos_activo": r[7]
                })
            return result
    except Exception as e:
        logger.error(f"Error Facturación por Arena: {e}")
        return []

def get_facturacion_por_arena_e_inversion_digital(query):
    """Facturación en arena DISTRIBUCION DE CONTENIDO - ON de empresas con inversión digital"""
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
    
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    logger.info("JARVIS Claude - Iniciando...")
    app.run(host="0.0.0.0", port=5000, debug=True)