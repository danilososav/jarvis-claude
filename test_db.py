
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv('config/.env')

DB_URL = f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASS')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DB')}"
engine = create_engine(DB_URL, pool_pre_ping=True)

# Test 1: BANCO FAMILIAR
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM dim_anunciante WHERE UPPER(nombre_canonico) LIKE '%BANCO FAMILIAR%'")).fetchone()
    print(f'BANCO FAMILIAR exists: {result[0]}')
    
    result = conn.execute(text("SELECT nombre_canonico, anunciante_id FROM dim_anunciante WHERE UPPER(nombre_canonico) LIKE '%BANCO FAMILIA%' LIMIT 1")).fetchone()
    if result:
        print(f'Found: {result}')
        
        # Test investment data
        inv = conn.execute(text(f"SELECT inversion_en_tv_abierta_2024_en_miles_usd FROM dim_anunciante_perfil WHERE anunciante_id = {result[1]}")).fetchone()
        print(f'Investment TV: {inv}')
        
        # Test facturación
        fact = conn.execute(text(f"SELECT SUM(facturacion) FROM fact_facturacion WHERE anunciante_id = {result[1]}")).fetchone()
        print(f'Facturacion: {fact}')

# Test 2: Cluster 4
print()
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM dim_anunciante_perfil WHERE cluster = '4'")).fetchone()
    print(f'Cluster 4 count: {result[0]}')
    
# Test 3: Decisión Marketing
print()
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM dim_anunciante_perfil WHERE el_departamento_de_marketing_toma_decisiones_auton IS NOT NULL")).fetchone()
    print(f'Marketing Decision count: {result[0]}')
    
# Test 4: Confianza
print()
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM dim_anunciante_perfil WHERE que_tan_desconfiada_es_la_empresa_cuanto_cuesta_ve ILIKE '%Muy desconfiada%'")).fetchone()
    print(f'Very Distrustful count: {result[0]}')


# Ejecuta
