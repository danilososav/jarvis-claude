"""
SCRIPT CORREGIDO: Eliminar duplicados con método más agresivo
"""

from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:123@localhost/jarvis")

def eliminar_duplicados_agresivo():
    """Método más directo para eliminar duplicados"""
    
    with engine.connect() as conn:
        print("🔥 ELIMINACIÓN AGRESIVA DE DUPLICADOS")
        print("=" * 50)
        
        # 1. Ver duplicados específicos
        print("📊 Analizando duplicados específicos...")
        
        stmt_duplicados = text("""
            WITH duplicados AS (
                SELECT 
                    cliente_original,
                    numero_factura,
                    fecha_fact,
                    facturacion,
                    COUNT(*) as copias,
                    MIN(id) as id_mantener
                FROM fact_facturacion 
                WHERE anio = 2025 
                    AND cliente_original IS NOT NULL
                GROUP BY cliente_original, numero_factura, fecha_fact, facturacion
                HAVING COUNT(*) > 1
            )
            SELECT 
                cliente_original,
                SUM(copias - 1) as registros_eliminar,
                SUM((copias - 1) * facturacion) as facturacion_duplicada
            FROM duplicados
            GROUP BY cliente_original
            ORDER BY facturacion_duplicada DESC
        """)
        
        duplicados_info = conn.execute(stmt_duplicados).fetchall()
        
        total_eliminar = 0
        total_facturacion_duplicada = 0
        
        for row in duplicados_info:
            print(f"   {row.cliente_original}: {row.registros_eliminar:,} duplicados")
            print(f"     Facturación duplicada: {float(row.facturacion_duplicada):,.0f} Gs")
            total_eliminar += row.registros_eliminar
            total_facturacion_duplicada += float(row.facturacion_duplicada)
        
        print(f"")
        print(f"📊 TOTAL A ELIMINAR: {total_eliminar:,} registros")
        print(f"💰 FACTURACIÓN DUPLICADA: {total_facturacion_duplicada:,.0f} Gs")
        
        if total_eliminar > 0:
            print("\n🗑️ EJECUTANDO ELIMINACIÓN...")
            
            # MÉTODO DIRECTO: Crear tabla temporal sin duplicados
            stmt_clean = text("""
                -- Crear tabla temporal con datos únicos
                CREATE TEMP TABLE fact_facturacion_clean AS
                SELECT DISTINCT ON (cliente_original, numero_factura, fecha_fact, facturacion) *
                FROM fact_facturacion 
                WHERE anio = 2025;
                
                -- Eliminar todos los registros 2025
                DELETE FROM fact_facturacion WHERE anio = 2025;
                
                -- Reinsertar datos limpios
                INSERT INTO fact_facturacion 
                SELECT * FROM fact_facturacion_clean;
                
                -- Limpiar tabla temporal
                DROP TABLE fact_facturacion_clean;
            """)
            
            conn.execute(stmt_clean)
            conn.commit()
            
            print("✅ Eliminación completada")
        
        # Verificar resultado final
        stmt_final = text("""
            SELECT 
                cliente_original,
                COUNT(*) as registros,
                SUM(facturacion) as facturacion_total
            FROM fact_facturacion 
            WHERE anio = 2025 
                AND cliente_original IN ('CERVEPAR S.A.', 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.')
            GROUP BY cliente_original
            ORDER BY facturacion_total DESC
        """)
        
        result_final = conn.execute(stmt_final).fetchall()
        
        print("")
        print("🎯 RESULTADO FINAL:")
        for row in result_final:
            print(f"   {row.cliente_original}")
            print(f"   Registros: {row.registros:,}")
            print(f"   Facturación: {float(row.facturacion_total):,.0f} Gs")
        
        print("")
        print("🎉 PROCESO COMPLETADO")
        print("✅ JARVIS ahora mostrará números correctos")

if __name__ == "__main__":
    eliminar_duplicados_agresivo()