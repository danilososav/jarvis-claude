"""
Script temporal para verificar consulta directa
"""

import psycopg2
from sqlalchemy import create_engine, text

# Configurar BD
engine = create_engine("postgresql://postgres:12345@localhost/jarvis")

print("🔍 VERIFICACIÓN DIRECTA BD:")
print("=" * 40)

try:
    with engine.connect() as conn:
        # Consulta TOP 5 exacta
        result = conn.execute(text("""
            SELECT 
                da.nombre_canonico, 
                COUNT(*) as registros,
                SUM(ff.facturacion) as total
            FROM fact_facturacion ff
            JOIN dim_anunciante da ON ff.anunciante_id = da.anunciante_id  
            WHERE ff.anio = 2025
            GROUP BY da.nombre_canonico
            ORDER BY total DESC
            LIMIT 5
        """))
        
        print("🏆 TOP 5 CLIENTES (BD Directa):")
        print("-" * 60)
        for i, row in enumerate(result, 1):
            print(f"{i}. {row.nombre_canonico}: {row.total:,.0f} Gs ({row.registros} reg)")
        
        print()
        
        # Verificación CERVEPAR específica
        result2 = conn.execute(text("""
            SELECT 
                da.nombre_canonico,
                COUNT(*) as registros, 
                SUM(ff.facturacion) as total
            FROM fact_facturacion ff
            JOIN dim_anunciante da ON ff.anunciante_id = da.anunciante_id  
            WHERE da.nombre_canonico = 'CERVEPAR S.A.'
                AND ff.anio = 2025
            GROUP BY da.nombre_canonico
        """))
        
        print("🍺 CERVEPAR ESPECÍFICO:")
        for row in result2:
            print(f"   {row.nombre_canonico}: {row.total:,.0f} Gs ({row.registros} registros)")
            
        # Verificación TELEFÓNICA específica  
        result3 = conn.execute(text("""
            SELECT 
                da.nombre_canonico,
                COUNT(*) as registros,
                SUM(ff.facturacion) as total  
            FROM fact_facturacion ff
            JOIN dim_anunciante da ON ff.anunciante_id = da.anunciante_id  
            WHERE da.nombre_canonico = 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.'
                AND ff.anio = 2025
            GROUP BY da.nombre_canonico
        """))
        
        print("📞 TELEFÓNICA ESPECÍFICO:")
        for row in result3:
            print(f"   {row.nombre_canonico}: {row.total:,.0f} Gs ({row.registros} registros)")
        
except Exception as e:
    print(f"❌ Error: {e}")

print()
print("✅ Verificación completada")
