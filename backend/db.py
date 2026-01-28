import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('config/.env')

DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB", "jarvis")
DB_USER = os.getenv("PG_USER", "postgres")
DB_PASS = os.getenv("PG_PASS", "postgres")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_anunciante"))
            count = result.scalar()
            print(f"✅ BD conectada: {count} clientes")
            return True
    except Exception as e:
        print(f"❌ Error BD: {e}")
        return False