"""
JARVIS - Backend Flask con PostgreSQL + Autenticación
Sistema BI conversacional para agencia de medios (Paraguay)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

# SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text

load_dotenv()

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
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# ==================== DATABASE ====================

DB_USER = os.getenv('PG_USER', 'postgres')
DB_PASS = os.getenv('PG_PASS', '12345')
DB_HOST = os.getenv('PG_HOST', 'localhost')
DB_PORT = os.getenv('PG_PORT', '5432')
DB_NAME = os.getenv('PG_DB', 'jarvis')

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL, pool_pre_ping=True)

# SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(255))
    role = Column(String(20), default='normal')
    created_at = Column(DateTime, default=datetime.now)

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    query = Column(Text)
    response = Column(Text)
    query_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

class TrainerFeedback(Base):
    __tablename__ = 'trainer_feedback'
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer)
    user_id = Column(Integer)
    original_response = Column(Text)
    corrected_response = Column(Text)
    feedback_type = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

# Create tables
try:
    Base.metadata.create_all(engine)
    logger.info("✅ Tablas creadas/verificadas")
except Exception as e:
    logger.error(f"Error creando tablas: {e}")

Session = sessionmaker(bind=engine)




# ==================== AUTHENTICATION ====================

SECRET_KEY = os.getenv('SECRET_KEY', 'jarvis-secret-key-2026')

def generate_token(user_id):
    """Genera JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verifica JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

def token_required(f):
    """Decorator para proteger endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        token = token.replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated

# ==================== QUERIES A LA BD ====================

def mock_claude_response(query_type, rows, user_query):
    """Respuestas inteligentes sin usar API Claude"""
    
    if query_type == "ranking":
        if rows:
            total_facturacion = sum(r.get("facturacion", 0) for r in rows)
            parts = [f"{i+1}. {r['cliente']}: {r['facturacion']:,.0f} Gs ({r.get('market_share', 0):.2f}%)" 
                    for i, r in enumerate(rows)]
            return f"Top {len(rows)} clientes por facturación:\n" + "\n".join(parts) + f"\nTotal: {total_facturacion:,.0f} Gs"
        return "No encontré datos de clientes."
    
    elif query_type == "facturacion":
        if rows:
            r = rows[0]
            return f"**{r['cliente']}** facturó **{r['facturacion']:,.0f} Gs** con un market share de {r.get('market_share', 0):.2f}%. Promedio mensual: {r.get('promedio_mensual', 0):,.0f} Gs."
        return "No tengo datos de facturación para ese cliente."
    
    else:
        return f"Query type: {query_type}. Registros encontrados: {len(rows)}."

def get_top_clientes_enriched(query):
    """Top 5 clientes por facturación"""
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion,
                    COUNT(*) as registros,
                    (SUM(f.facturacion) / NULLIF((SELECT SUM(facturacion) FROM fact_facturacion WHERE facturacion > 0), 0) * 100)::float as market_share
                FROM dim_anunciante d
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id
                WHERE f.facturacion > 0
                GROUP BY d.anunciante_id, d.nombre_canonico
                HAVING SUM(f.facturacion) > 0
                ORDER BY facturacion DESC
                LIMIT 5
            """)
            rows = conn.execute(stmt).fetchall()
            
            result = []
            for r in rows:
                result.append({
                    "cliente": r[0] or "Sin nombre",
                    "facturacion": float(r[1]) if r[1] else 0,
                    "registros": int(r[2]) if r[2] else 0,
                    "market_share": float(r[3]) if r[3] else 0
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

# ==================== ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"status": "✅ OK", "db": "connected"}), 200
    except:
        return jsonify({"status": "❌ ERROR", "db": "disconnected"}), 500

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Username y password requeridos'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password mínimo 6 caracteres'}), 400
        
        session = Session()
        
        # Verificar si existe
        existing = session.query(User).filter_by(username=username).first()
        if existing:
            session.close()
            return jsonify({'error': 'Usuario ya existe'}), 409
        
        # Crear usuario
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role='normal'
        )
        session.add(user)
        session.commit()
        user_id = user.id
        session.close()
        
        token = generate_token(user_id)
        
        logger.info(f"✅ Usuario registrado: {username}")
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'username': username,
            'role': 'normal',
            'token': token
        }), 201
        
    except Exception as e:
        logger.error(f"Error registrando usuario: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login de usuario"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Username y password requeridos'}), 400
        
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        session.close()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        token = generate_token(user.id)
        
        logger.info(f"✅ Login: {username}")
        
        return jsonify({
            'success': True,
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'token': token
        }), 200
        
    except Exception as e:
        logger.error(f"Error en login: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/verify', methods=['GET'])
@token_required
def verify_user(user_id):
    """Verificar token y obtener info del usuario"""
    try:
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'success': True,
            'user_id': user.id,
            'username': user.username,
            'role': user.role
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== QUERY ENDPOINTS ====================

@app.route('/api/chat/history', methods=['GET'])
@token_required
def get_chat_history(user_id):
    """Obtener historial de chat del usuario"""
    try:
        session = Session()
        
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

@app.route('/api/query', methods=['POST'])
@token_required
def query(user_id):
    """Procesar query con detección automática de tipo"""
    data = request.json
    user_query = data.get('query', '').strip()
    
    if not user_query:
        return jsonify({"error": "Query vacío"}), 400
    
    try:
        query_lower = user_query.lower()
        rows = []
        query_type = "generico"
        
        # DETECCIÓN INTELIGENTE (Mejorada)
        if any(w in query_lower for w in ["top", "ranking", "principal", "importante", "mayor", "más", "clientes"]):
            if any(w in query_lower for w in ["factur", "ingresos", "venta"]):
                query_type = "ranking"
                rows = get_top_clientes_enriched(user_query)
                logger.info(f"🔍 Detectado: ranking - rows: {len(rows)}")
            else:
                query_type = "ranking"
                rows = get_top_clientes_enriched(user_query)
                logger.info(f"🔍 Detectado: ranking - rows: {len(rows)}")

        elif any(w in query_lower for w in ["cuánto", "cuanto", "factur", "how much"]):
            query_type = "facturacion"
            rows = get_facturacion_enriched(user_query)
            logger.info(f"🔍 Detectado: facturacion - rows: {len(rows)}")
        else:
            return jsonify({"success": False, "response": "Consulta no reconocida. Prueba: 'Top 5 clientes', 'Cuánto facturó CERVEPAR?'"}), 200
        
        # Mock Claude (Sin API)
        response_text = mock_claude_response(query_type, rows, user_query)
        
        # Guardar en BD
        session = Session()
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
    

@app.route('/api/chat/history/<int:conv_id>', methods=['DELETE'])
@token_required
def delete_conversation(user_id, conv_id):
    """Eliminar una conversación"""
    try:
        session = Session()
        
        conversation = session.query(Conversation).filter_by(
            id=conv_id, 
            user_id=user_id
        ).first()
        
        if not conversation:
            session.close()
            return jsonify({'error': 'Conversación no encontrada'}), 404
        
        session.delete(conversation)
        session.commit()
        session.close()
        
        logger.info(f"✅ Conversación {conv_id} eliminada")
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        logger.error(f"Error eliminando conversación: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/trainer/feedback', methods=['POST'])
@token_required
def submit_trainer_feedback(user_id):
    """Enviar corrección/feedback como trainer"""
    session = None
    try:
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        
        if not user or user.role != 'trainer':
            return jsonify({'error': 'Solo trainers pueden enviar feedback'}), 403
        
        data = request.json
        feedback = TrainerFeedback(
            conversation_id=data.get('conversation_id'),
            user_id=user_id,
            original_response=data.get('original_response'),
            corrected_response=data.get('corrected_response'),
            feedback_type=data.get('feedback_type', 'correction'),
            notes=data.get('notes', '')
        )
        session.add(feedback)
        session.commit()
        feedback_id = feedback.id
        
        logger.info(f"✅ Trainer feedback guardado: {feedback_id}")
        
        return jsonify({'success': True, 'feedback_id': feedback_id}), 201
        
    except Exception as e:
        logger.error(f"Error en trainer feedback: {e}")
        if session:
            session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if session:
            session.close()

            
@app.route('/api/trainer/feedback', methods=['GET'])
@token_required
def get_trainer_feedback(user_id):
    """Obtener feedback guardado"""
    try:
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        
        if not user or user.role != 'trainer':
            session.close()
            return jsonify({'error': 'Solo trainers pueden ver feedback'}), 403
        
            feedbacks = session.query(TrainerFeedback)\
            .filter_by(user_id=user_id)\
            .order_by(TrainerFeedback.created_at.desc())\
            .limit(100)\
            .all()
        
        result = [{
            "id": f.id,
            "conversation_id": f.conversation_id,
            "original_response": f.original_response[:100],
            "corrected_response": f.corrected_response[:100],
            "feedback_type": f.feedback_type,
            "notes": f.notes,
            "created_at": f.created_at.isoformat()
        } for f in feedbacks]
        
        session.close()
        return jsonify({'success': True, 'feedbacks': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 JARVIS Backend con Autenticación iniciando...")
    app.run(host='0.0.0.0', port=5000, debug=True)