import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import engine, test_connection
from claude_handler import ClaudeHandler
from sqlalchemy import text
from datetime import datetime, timedelta

load_dotenv('config/.env')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
claude = ClaudeHandler(ANTHROPIC_API_KEY)

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
        
        if any(w in query_lower for w in ["top", "ranking", "principal", "importante", "mayor", "más"]):
            query_type = "ranking"
            rows = get_top_clientes_enriched(user_query)
        elif any(w in query_lower for w in ["cuánto", "factur", "ganó", "vendió", "hizo"]):
            query_type = "facturacion"
            rows = get_facturacion_enriched(user_query)
        elif "vs" in query_lower or "versus" in query_lower:
            query_type = "comparacion"
            rows = get_comparacion_enriched(user_query)
        elif any(w in query_lower for w in ["perfil", "quién es", "como es", "empresa"]):
            query_type = "perfil"
            rows = get_perfil_enriched(user_query)
        elif any(w in query_lower for w in ["tendencia", "crecimiento", "variación", "cambio"]):
            query_type = "tendencia"
            rows = get_tendencia_enriched(user_query)
        else:
            return jsonify({"success": False, "response": "Consulta no reconocida. Prueba: 'Top 5 clientes', 'Cuánto facturó CERVEPAR?', 'CERVEPAR vs TELEFONICA'"}), 200
        
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
    palabras = query.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    
    if not cliente:
        return []
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion_total,
                    COUNT(DISTINCT (f.anio::text || '-' || f.mes::text)) as meses_activo
                    COUNT(DISTINCT f.familia) as familias_productos,
                    MAX(f.anio) as ultimo_año,
                    AVG(f.facturacion)::float as promedio_mensual
                FROM dim_anunciante d
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id AND f.facturacion > 0
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            return [{"cliente": r[0], "facturacion": float(r[1]) if r[1] else 0, "meses_activo": r[2] or 0, "familias": r[3] or 0, "ultimo_año": r[4], "promedio_mensual": float(r[5]) if r[5] else 0} for r in rows]
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

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    logger.info("JARVIS Claude - Iniciando...")
    app.run(host="0.0.0.0", port=5000, debug=True)