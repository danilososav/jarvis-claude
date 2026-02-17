"""
DIAGNÓSTICO FINAL: Ver exactamente qué datos hay en la BD
"""

from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:123@localhost/jarvis")

def diagnostico_bd_final():
    """Ver exactamente qué está pasando en la BD"""
    
    print("🚨 DIAGNÓSTICO FINAL DE LA BD")
    print("=" * 50)
    
    with engine.connect() as conn:
        # 1. Contar total de registros
        total_query = text("SELECT COUNT(*), SUM(facturacion) FROM fact_facturacion")
        total = conn.execute(total_query).fetchone()
        print(f"📊 Total BD: {total[0]:,} registros, {float(total[1]):,.0f} Gs")
        
        # 2. Ver por año
        year_query = text("SELECT anio, COUNT(*), SUM(facturacion) FROM fact_facturacion GROUP BY anio ORDER BY anio")
        years = conn.execute(year_query).fetchall()
        print("\n📅 Por año:")
        for row in years:
            print(f"   {row.anio}: {row.count:,} registros, {float(row.sum):,.0f} Gs")
        
        # 3. Ver CERVEPAR específico - TODOS los registros
        cervepar_query = text("""
            SELECT 
                facturacion,
                COUNT(*) as cantidad_registros_con_este_valor
            FROM fact_facturacion 
            WHERE cliente_original = 'CERVEPAR S.A.' 
            GROUP BY facturacion
            ORDER BY facturacion DESC
            LIMIT 10
        """)
        
        print("\n🍺 CERVEPAR - Valores de facturación:")
        cervepar_values = conn.execute(cervepar_query).fetchall()
        total_cervepar = 0
        for row in cervepar_values:
            print(f"   {float(row.facturacion):,.0f} Gs × {row.cantidad_registros_con_este_valor} registros")
            total_cervepar += float(row.facturacion) * row.cantidad_registros_con_este_valor
        
        print(f"\n🎯 CERVEPAR Total calculado: {total_cervepar:,.0f} Gs")
        
        # 4. Ver algunos registros específicos de CERVEPAR
        sample_query = text("""
            SELECT facturacion, numero_factura, fecha_fact
            FROM fact_facturacion 
            WHERE cliente_original = 'CERVEPAR S.A.' 
            ORDER BY facturacion DESC
            LIMIT 5
        """)
        
        print("\n🔍 Muestra de registros CERVEPAR:")
        sample = conn.execute(sample_query).fetchall()
        for row in sample:
            print(f"   {float(row.facturacion):,.0f} Gs - Factura: {row.numero_factura} - Fecha: {row.fecha_fact}")
        
        # 5. Verificar si hay registros duplicados
        dup_query = text("""
            SELECT 
                cliente_original,
                numero_factura,
                fecha_fact,
                facturacion,
                COUNT(*) as duplicados
            FROM fact_facturacion 
            WHERE cliente_original = 'CERVEPAR S.A.'
            GROUP BY cliente_original, numero_factura, fecha_fact, facturacion
            HAVING COUNT(*) > 1
            ORDER BY duplicados DESC
            LIMIT 5
        """)
        
        print("\n🔍 Registros duplicados CERVEPAR:")
        duplicados = conn.execute(dup_query).fetchall()
        if duplicados:
            for row in duplicados:
                print(f"   Factura {row.numero_factura}: {row.duplicados} copias de {float(row.facturacion):,.0f} Gs")
        else:
            print("   No hay duplicados evidentes")
        
        # 6. Total correcto esperado vs obtenido
        correct_query = text("""
            SELECT COUNT(*), SUM(facturacion) 
            FROM fact_facturacion 
            WHERE cliente_original = 'CERVEPAR S.A.'
        """)
        
        cervepar_total = conn.execute(correct_query).fetchone()
        print(f"\n📊 CERVEPAR BD: {cervepar_total[0]:,} registros, {float(cervepar_total[1]):,.0f} Gs")
        print(f"📊 CERVEPAR Excel esperado: 1,136 registros, 26,057,164,652 Gs")
        
        diff_reg = cervepar_total[0] - 1136
        diff_fact = float(cervepar_total[1]) - 26057164652
        
        print(f"📊 Diferencia: {diff_reg} registros, {diff_fact:,.0f} Gs")

if __name__ == "__main__":
    diagnostico_bd_final()
