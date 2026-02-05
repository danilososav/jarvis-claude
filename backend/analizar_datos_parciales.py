"""
Identificar clientes con datos parciales para testing
"""

import sys
sys.path.append('/home/claude')

from sqlalchemy import create_engine, text
import os

# Configuración DB
DB_USER = 'postgres'
DB_PASS = '12345'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'jarvis'

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL, pool_pre_ping=True)

try:
    print("🔍 ANÁLISIS DE DATOS PARCIALES")
    print("="*60)
    
    with engine.connect() as conn:
        # Clientes con facturación pero SIN ranking DNIT
        print("\n1️⃣ Clientes CON facturación pero SIN ranking DNIT:")
        print("-" * 50)
        
        result = conn.execute(text("""
            SELECT 
                a.nombre_canonico,
                ROUND(SUM(f.facturacion), 0) as facturacion_total,
                COUNT(f.*) as registros_fact
            FROM dim_anunciante a
            JOIN fact_facturacion f ON a.anunciante_id = f.anunciante_id
            LEFT JOIN dim_posicionamiento_dnit d ON a.anunciante_id = d.anunciante_id
            WHERE d.anunciante_id IS NULL  -- SIN ranking DNIT
            GROUP BY a.anunciante_id, a.nombre_canonico
            ORDER BY facturacion_total DESC
            LIMIT 5
        """)).fetchall()
        
        for i, row in enumerate(result, 1):
            print(f"   {i}. {row[0]}: {row[1]:,.0f} Gs ({row[2]} registros)")
        
        # Clientes con facturación pero SIN inversión en medios
        print("\n2️⃣ Clientes CON facturación pero SIN inversión en medios:")
        print("-" * 50)
        
        result2 = conn.execute(text("""
            SELECT 
                a.nombre_canonico,
                ROUND(SUM(f.facturacion), 0) as facturacion_total,
                COUNT(f.*) as registros_fact
            FROM dim_anunciante a
            JOIN fact_facturacion f ON a.anunciante_id = f.anunciante_id
            LEFT JOIN fact_inversion_medios i ON a.anunciante_id = i.anunciante_id
            WHERE i.anunciante_id IS NULL  -- SIN inversión medios
            GROUP BY a.anunciante_id, a.nombre_canonico
            ORDER BY facturacion_total DESC
            LIMIT 5
        """)).fetchall()
        
        for i, row in enumerate(result2, 1):
            print(f"   {i}. {row[0]}: {row[1]:,.0f} Gs ({row[2]} registros)")
        
        # Clientes solo en ranking DNIT pero sin facturación
        print("\n3️⃣ Clientes CON ranking DNIT pero SIN facturación:")
        print("-" * 50)
        
        result3 = conn.execute(text("""
            SELECT 
                d.razon_social,
                d.ranking,
                d.aporte_gs
            FROM dim_posicionamiento_dnit d
            LEFT JOIN dim_anunciante a ON d.anunciante_id = a.anunciante_id
            WHERE a.anunciante_id IS NULL  -- SIN facturación (no están en dim_anunciante)
            ORDER BY d.ranking
            LIMIT 5
        """)).fetchall()
        
        for i, row in enumerate(result3, 1):
            print(f"   {i}. {row[0]} (Ranking #{row[1]}): {row[2]:,.0f} Gs aporte")
        
        # Resumen estadístico
        print("\n" + "="*60)
        print("📊 RESUMEN ESTADÍSTICO:")
        print("="*60)
        
        stats = conn.execute(text("""
            SELECT 
                'Total clientes en dim_anunciante' as tabla,
                COUNT(*) as cantidad
            FROM dim_anunciante
            UNION ALL
            SELECT 
                'Clientes con facturación',
                COUNT(DISTINCT anunciante_id)
            FROM fact_facturacion
            UNION ALL
            SELECT 
                'Clientes con inversión medios',
                COUNT(DISTINCT anunciante_id)
            FROM fact_inversion_medios
            WHERE anunciante_id IS NOT NULL
            UNION ALL
            SELECT 
                'Clientes con ranking DNIT',
                COUNT(DISTINCT anunciante_id)
            FROM dim_posicionamiento_dnit
            WHERE anunciante_id IS NOT NULL
        """)).fetchall()
        
        for row in stats:
            print(f"   {row[0]}: {row[1]}")
    
    print("\n✅ Análisis completado")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

