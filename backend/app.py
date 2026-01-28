import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import engine, test_connection
from claude_handler import ClaudeHandler
from sqlalchemy import text

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
        
        if "top" in query_lower or "ranking" in query_lower:
            query_type = "ranking"
            rows = get_top_clientes(user_query)
        elif "cuánto" in query_lower or "factur" in query_lower:
            query_type = "facturacion"
            rows = get_facturacion(user_query)
        elif "vs" in query_lower or "versus" in query_lower:
            query_type = "comparacion"
            rows = get_comparacion(user_query)
        elif "perfil" in query_lower or "quién es" in query_lower:
            query_type = "perfil"
            rows = get_perfil(user_query)
        else:
            return jsonify({"success": False, "response": "Consulta no reconocida. Prueba: 'Top 5 clientes', 'Cuánto facturó CERVEPAR?'"}), 200
        
        response_text = claude.enhance_response(user_query, rows, query_type)
        if not response_text:
            response_text = str(rows)
        
        return jsonify({"success": True, "response": response_text, "query_type": query_type, "rows": rows}), 200
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

def get_top_clientes(query, limit=5):
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico as anunciante,
                    SUM(f.facturacion)::float as total_facturacion
                FROM fact_facturacion f
                JOIN dim_anunciante d ON d.anunciante_id = f.anunciante_id
                WHERE f.facturacion > 0
                GROUP BY d.anunciante_id, d.nombre_canonico
                ORDER BY total_facturacion DESC
                LIMIT :limit
            """)
            rows = conn.execute(stmt, {"limit": limit}).fetchall()
            return [{"anunciante": r[0], "facturacion": float(r[1])} for r in rows]
    except Exception as e:
        logger.error(f"Error Top: {e}")
        return []

def get_facturacion(query):
    palabras = query.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    if not cliente:
        return []
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico as anunciante,
                    SUM(f.facturacion)::float as total_facturacion
                FROM fact_facturacion f
                JOIN dim_anunciante d ON d.anunciante_id = f.anunciante_id
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                AND f.facturacion > 0
                GROUP BY d.anunciante_id, d.nombre_canonico
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            return [{"anunciante": r[0], "facturacion": float(r[1])} for r in rows]
    except Exception as e:
        logger.error(f"Error Facturacion: {e}")
        return []

def get_comparacion(query):
    partes = query.lower().split("vs")
    if len(partes) != 2:
        return []
    cliente1 = partes[0].strip().split()[-1].upper()
    cliente2 = partes[1].strip().split()[0].upper()
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico as anunciante,
                    SUM(f.facturacion)::float as total_facturacion
                FROM fact_facturacion f
                JOIN dim_anunciante d ON d.anunciante_id = f.anunciante_id
                WHERE (UPPER(d.nombre_canonico) LIKE UPPER(:cliente1) OR UPPER(d.nombre_canonico) LIKE UPPER(:cliente2))
                AND f.facturacion > 0
                GROUP BY d.anunciante_id, d.nombre_canonico
            """)
            rows = conn.execute(stmt, {"cliente1": f"%{cliente1}%", "cliente2": f"%{cliente2}%"}).fetchall()
            return [{"anunciante": r[0], "facturacion": float(r[1])} for r in rows]
    except Exception as e:
        logger.error(f"Error Comparacion: {e}")
        return []

def get_perfil(query):
    palabras = query.split()
    cliente = " ".join([p for p in palabras if p.isupper()])
    if not cliente:
        return []
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion
                FROM dim_anunciante d
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id
                WHERE UPPER(d.nombre_canonico) LIKE UPPER(:cliente)
                GROUP BY d.anunciante_id, d.nombre_canonico
            """)
            rows = conn.execute(stmt, {"cliente": f"%{cliente}%"}).fetchall()
            return [{"anunciante": r[0], "facturacion": float(r[1]) if r[1] else 0} for r in rows]
    except Exception as e:
        logger.error(f"Error Perfil: {e}")
        return []

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    logger.info("JARVIS Claude - Iniciando...")
    app.run(host="0.0.0.0", port=5000, debug=True)