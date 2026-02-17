"""
LIMPIEZA FINAL: Eliminar TODO excepto 2025 recién cargado
"""

from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:danilo123@localhost/jarvis_bi")

def limpieza_final():
    """Eliminar todo lo que no sea 2025"""
    
    print("🔥 LIMPIEZA FINAL - SOLO 2025")
    print("=" * 40)
    
    with engine.connect() as conn:
        # Ver qué años hay
        years_query = text("SELECT anio, COUNT(*) FROM fact_facturacion GROUP BY anio ORDER BY anio")
        years_result = conn.execute(years_query).fetchall()
        
        print("📊 AÑOS EN LA BD:")
        total_otros = 0
        for row in years_result:
            print(f"   {row.anio}: {row.count:,} registros")
            if row.anio != 2025:
                total_otros += row.count
        
        print(f"\n🗑️ Registros a eliminar (no-2025): {total_otros:,}")
        
        if total_otros > 0:
            # Eliminar TODO lo que no sea 2025
            delete_query = text("DELETE FROM fact_facturacion WHERE anio != 2025 OR anio IS NULL")
            result = conn.execute(delete_query)
            eliminados = result.rowcount
            conn.commit()
            
            print(f"✅ Eliminados: {eliminados:,} registros históricos")
        
        # Verificar resultado
        verify_query = text("""
            SELECT 
                cliente_original,
                COUNT(*) as registros,
                SUM(facturacion) as facturacion_total
            FROM fact_facturacion 
            WHERE cliente_original IN ('CERVEPAR S.A.', 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.')
            GROUP BY cliente_original
            ORDER BY facturacion_total DESC
        """)
        
        verification = conn.execute(verify_query).fetchall()
        
        print("\n🎯 VERIFICACIÓN POST-LIMPIEZA:")
        for row in verification:
            print(f"   {row.cliente_original}")
            print(f"   Registros: {row.registros:,}")
            print(f"   Facturación: {float(row.facturacion_total):,.0f} Gs")
        
        # Total final
        total_query = text("SELECT COUNT(*), SUM(facturacion) FROM fact_facturacion")
        total_result = conn.execute(total_query).fetchone()
        
        print(f"\n📊 TOTAL FINAL BD: {total_result[0]:,} registros")
        print(f"💰 FACTURACIÓN TOTAL: {float(total_result[1]):,.0f} Gs")
        
        # Comparar con Excel esperado
        excel_total = 134318231314.87
        bd_total = float(total_result[1])
        
        diferencia = abs(excel_total - bd_total)
        
        if diferencia < 100:  # Menos de 100 Gs de diferencia
            print("\n🎉 ¡PERFECTO! BD coincide con Excel")
            print("✅ JARVIS ahora será exacto")
        else:
            print(f"\n⚠️ Diferencia: {diferencia:.2f} Gs")

if __name__ == "__main__":
    limpieza_final()
