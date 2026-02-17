"""
Diagnóstico avanzado - Encontrar la causa de datos inflados
"""

from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:123@localhost/jarvis")

def diagnostico_completo():
    """Diagnóstico completo de duplicación de datos"""
    
    with engine.connect() as conn:
        print("🚨 DIAGNÓSTICO COMPLETO DE DUPLICACIÓN")
        print("=" * 60)
        
        # 1. VERIFICAR DATOS DIRECTOS EN fact_facturacion
        print("1️⃣ DATOS DIRECTOS EN fact_facturacion:")
        print("-" * 40)
        
        stmt1 = text("""
            SELECT 
                cliente_original,
                COUNT(*) as registros,
                SUM(facturacion) as total_facturacion
            FROM fact_facturacion 
            WHERE anio = 2025 
                AND cliente_original IN ('CERVEPAR S.A.', 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.')
            GROUP BY cliente_original
            ORDER BY total_facturacion DESC
        """)
        
        result1 = conn.execute(stmt1).fetchall()
        for row in result1:
            print(f"   {row.cliente_original}")
            print(f"   Registros: {row.registros:,}")
            print(f"   Facturación: {float(row.total_facturacion):,.0f} Gs")
            print()
        
        # 2. VERIFICAR CON JOIN dim_anunciante
        print("2️⃣ DATOS CON JOIN dim_anunciante:")
        print("-" * 40)
        
        stmt2 = text("""
            SELECT 
                d.nombre_canonico,
                f.cliente_original,
                COUNT(*) as registros,
                SUM(f.facturacion) as total_facturacion
            FROM dim_anunciante d
            JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id
            WHERE f.anio = 2025 
                AND d.nombre_canonico IN ('CERVEPAR S.A.', 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.')
            GROUP BY d.nombre_canonico, f.cliente_original
            ORDER BY total_facturacion DESC
        """)
        
        result2 = conn.execute(stmt2).fetchall()
        for row in result2:
            print(f"   dim_anunciante: {row.nombre_canonico}")
            print(f"   fact_facturacion: {row.cliente_original}")
            print(f"   Registros: {row.registros:,}")
            print(f"   Facturación: {float(row.total_facturacion):,.0f} Gs")
            print()
        
        # 3. VERIFICAR MÚLTIPLES anunciante_id PARA EL MISMO CLIENTE
        print("3️⃣ MÚLTIPLES anunciante_id PARA EL MISMO CLIENTE:")
        print("-" * 40)
        
        stmt3 = text("""
            SELECT 
                cliente_original,
                anunciante_id,
                COUNT(*) as registros,
                SUM(facturacion) as total_facturacion
            FROM fact_facturacion 
            WHERE anio = 2025 
                AND cliente_original IN ('CERVEPAR S.A.', 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.')
            GROUP BY cliente_original, anunciante_id
            ORDER BY cliente_original, anunciante_id
        """)
        
        result3 = conn.execute(stmt3).fetchall()
        for row in result3:
            print(f"   {row.cliente_original} (ID: {row.anunciante_id})")
            print(f"   Registros: {row.registros:,}")
            print(f"   Facturación: {float(row.total_facturacion):,.0f} Gs")
            print()
        
        # 4. VERIFICAR LEFT JOIN vs INNER JOIN
        print("4️⃣ COMPARACIÓN LEFT JOIN vs INNER JOIN:")
        print("-" * 40)
        
        # LEFT JOIN (actual en el código)
        stmt4a = text("""
            SELECT 
                d.nombre_canonico,
                SUM(f.facturacion) as total_facturacion,
                COUNT(*) as registros
            FROM dim_anunciante d
            LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id
            WHERE f.facturacion > 0 AND f.anio = 2025
                AND d.nombre_canonico IN ('CERVEPAR S.A.', 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.')
            GROUP BY d.nombre_canonico
            ORDER BY total_facturacion DESC
        """)
        
        print("   LEFT JOIN:")
        result4a = conn.execute(stmt4a).fetchall()
        for row in result4a:
            print(f"     {row.nombre_canonico}: {float(row.total_facturacion):,.0f} Gs ({row.registros} reg)")
        
        # INNER JOIN
        stmt4b = text("""
            SELECT 
                d.nombre_canonico,
                SUM(f.facturacion) as total_facturacion,
                COUNT(*) as registros
            FROM dim_anunciante d
            INNER JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id
            WHERE f.facturacion > 0 AND f.anio = 2025
                AND d.nombre_canonico IN ('CERVEPAR S.A.', 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.')
            GROUP BY d.nombre_canonico
            ORDER BY total_facturacion DESC
        """)
        
        print("   INNER JOIN:")
        result4b = conn.execute(stmt4b).fetchall()
        for row in result4b:
            print(f"     {row.nombre_canonico}: {float(row.total_facturacion):,.0f} Gs ({row.registros} reg)")

if __name__ == "__main__":
    diagnostico_completo()
