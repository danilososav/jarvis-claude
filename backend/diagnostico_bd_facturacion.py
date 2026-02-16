"""
DIAGNÓSTICO: Problema de facturación en JARVIS
Verificar por qué las consultas retornan 0 datos
"""

from sqlalchemy import text, create_engine
import logging

def diagnosticar_bd():
    """
    Diagnóstico completo de la base de datos
    """
    
    print("🔍 DIAGNÓSTICO DE BASE DE DATOS")
    print("="*50)
    
    try:
        # Importar configuración desde app.py
        from app import engine
        
        print("✅ Conexión a base de datos establecida")
        
        with engine.connect() as conn:
            
            # 1. Verificar si existen las tablas
            print("\n📋 VERIFICANDO TABLAS:")
            
            tables = ['fact_facturacion', 'dim_anunciante_perfil', 'dim_posicionamiento_dnit']
            
            for table in tables:
                try:
                    count_query = text(f"SELECT COUNT(*) as total FROM {table}")
                    result = conn.execute(count_query).fetchone()
                    print(f"   {table}: {result.total:,} registros")
                except Exception as e:
                    print(f"   {table}: ❌ ERROR - {e}")
            
            # 2. Verificar CERVEPAR específicamente
            print(f"\n🎯 VERIFICANDO CERVEPAR:")
            
            # Buscar en dim_anunciante_perfil
            cervepar_query = text("""
                SELECT anunciante_id, nombre_anunciante 
                FROM dim_anunciante_perfil 
                WHERE UPPER(nombre_anunciante) LIKE '%CERVEPAR%'
                LIMIT 5
            """)
            
            results = conn.execute(cervepar_query).fetchall()
            
            if results:
                print("   Encontrado en dim_anunciante_perfil:")
                for row in results:
                    print(f"     ID: {row.anunciante_id} | Nombre: {row.nombre_anunciante}")
                    
                    # 3. Verificar facturación para cada ID encontrado
                    print(f"\n💰 VERIFICANDO FACTURACIÓN PARA ID {row.anunciante_id}:")
                    
                    facturacion_query = text("""
                        SELECT 
                            COUNT(*) as registros,
                            SUM(facturacion) as total_facturacion,
                            SUM(revenue) as total_revenue,
                            MIN(fecha_fact) as fecha_min,
                            MAX(fecha_fact) as fecha_max
                        FROM fact_facturacion 
                        WHERE anunciante_id = :anunciante_id
                    """)
                    
                    fact_result = conn.execute(facturacion_query, {"anunciante_id": row.anunciante_id}).fetchone()
                    
                    print(f"     Registros: {fact_result.registros}")
                    print(f"     Facturación: {fact_result.total_facturacion or 0:,.0f} Gs")
                    print(f"     Revenue: {fact_result.total_revenue or 0:,.0f} Gs")
                    print(f"     Fecha rango: {fact_result.fecha_min} - {fact_result.fecha_max}")
                    
                    if fact_result.registros > 0:
                        print("     ✅ TIENE DATOS DE FACTURACIÓN")
                        
                        # Mostrar algunos registros ejemplo
                        sample_query = text("""
                            SELECT facturacion, revenue, division, arena, fecha_fact
                            FROM fact_facturacion 
                            WHERE anunciante_id = :anunciante_id
                            ORDER BY fecha_fact DESC
                            LIMIT 3
                        """)
                        
                        samples = conn.execute(sample_query, {"anunciante_id": row.anunciante_id}).fetchall()
                        
                        print("     📊 EJEMPLOS DE REGISTROS:")
                        for sample in samples:
                            print(f"       {sample.fecha_fact} | {sample.facturacion:,.0f} Gs | {sample.division} | {sample.arena}")
                    else:
                        print("     ❌ NO TIENE DATOS DE FACTURACIÓN")
            else:
                print("   ❌ CERVEPAR no encontrado en dim_anunciante_perfil")
                
                # Buscar variaciones
                print("   🔍 Buscando variaciones...")
                
                variations_query = text("""
                    SELECT anunciante_id, nombre_anunciante 
                    FROM dim_anunciante_perfil 
                    WHERE UPPER(nombre_anunciante) LIKE '%CERV%'
                       OR UPPER(nombre_anunciante) LIKE '%BEER%'
                       OR UPPER(nombre_anunciante) LIKE '%PILSEN%'
                    LIMIT 10
                """)
                
                variations = conn.execute(variations_query).fetchall()
                
                if variations:
                    print("   📋 Empresas relacionadas encontradas:")
                    for var in variations:
                        print(f"     ID: {var.anunciante_id} | {var.nombre_anunciante}")
                else:
                    print("   ❌ No se encontraron empresas relacionadas")
            
            # 4. Verificar top clientes con facturación
            print(f"\n🏆 TOP 5 CLIENTES POR FACTURACIÓN:")
            
            top_query = text("""
                SELECT 
                    p.nombre_anunciante,
                    SUM(f.facturacion) as total_facturacion,
                    COUNT(f.*) as registros
                FROM fact_facturacion f
                JOIN dim_anunciante_perfil p ON f.anunciante_id = p.anunciante_id
                GROUP BY p.anunciante_id, p.nombre_anunciante
                HAVING SUM(f.facturacion) > 0
                ORDER BY SUM(f.facturacion) DESC
                LIMIT 5
            """)
            
            top_results = conn.execute(top_query).fetchall()
            
            if top_results:
                for i, row in enumerate(top_results, 1):
                    print(f"   {i}. {row.nombre_anunciante}: {row.total_facturacion:,.0f} Gs ({row.registros} registros)")
            else:
                print("   ❌ No se encontraron clientes con facturación > 0")
                
    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")
        return False
        
    return True

if __name__ == "__main__":
    print("🚨 DIAGNÓSTICO DE FACTURACIÓN - JARVIS BI 360°")
    print("="*60)
    print("Identificando por qué CERVEPAR retorna 0 datos\n")
    
    success = diagnosticar_bd()
    
    if success:
        print(f"\n✅ DIAGNÓSTICO COMPLETADO")
        print("📋 Revisa los resultados para identificar el problema")
    else:
        print(f"\n❌ DIAGNÓSTICO FALLÓ")
        print("🔧 Verifica la conexión a base de datos")

