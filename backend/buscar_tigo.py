"""
TEST ESPECÍFICO: ¿Cómo está registrado TIGO en la BD?
"""

from app import engine
from sqlalchemy import text

def buscar_tigo_en_bd():
    """
    Buscar todas las variantes de TIGO en la base de datos
    """
    
    print("🔍 BÚSQUEDA DE TIGO EN BD")
    print("="*40)
    
    try:
        with engine.connect() as conn:
            
            # 1. Buscar cualquier cosa que contenga "tigo"
            stmt = text("""
                SELECT 
                    anunciante_id,
                    nombre_anunciante,
                    rubro_principal
                FROM dim_anunciante_perfil
                WHERE LOWER(nombre_anunciante) LIKE '%tigo%'
                ORDER BY nombre_anunciante
            """)
            
            results = conn.execute(stmt).fetchall()
            
            print("📋 RESULTADOS CON 'TIGO':")
            if results:
                for row in results:
                    print(f"   ID: {row.anunciante_id} | Nombre: {row.nombre_anunciante} | Rubro: {row.rubro_principal}")
            else:
                print("   ❌ No se encontró ningún registro con 'tigo'")
            
            # 2. Buscar variantes de telecos
            stmt2 = text("""
                SELECT 
                    anunciante_id,
                    nombre_anunciante,
                    rubro_principal
                FROM dim_anunciante_perfil
                WHERE LOWER(nombre_anunciante) LIKE '%telecom%'
                   OR LOWER(nombre_anunciante) LIKE '%telefon%'
                   OR LOWER(nombre_anunciante) LIKE '%movil%'
                   OR LOWER(nombre_anunciante) LIKE '%celular%'
                ORDER BY nombre_anunciante
            """)
            
            results2 = conn.execute(stmt2).fetchall()
            
            print(f"\n📋 OTRAS TELECOS:")
            if results2:
                for row in results2:
                    print(f"   ID: {row.anunciante_id} | Nombre: {row.nombre_anunciante}")
            else:
                print("   ❌ No se encontraron telecos")
            
            # 3. Top 10 clientes por nombre para ver qué hay
            stmt3 = text("""
                SELECT 
                    anunciante_id,
                    nombre_anunciante
                FROM dim_anunciante_perfil
                WHERE nombre_anunciante IS NOT NULL
                ORDER BY anunciante_id
                LIMIT 10
            """)
            
            results3 = conn.execute(stmt3).fetchall()
            
            print(f"\n📋 SAMPLE PRIMEROS 10 CLIENTES:")
            for row in results3:
                print(f"   ID: {row.anunciante_id} | Nombre: {row.nombre_anunciante}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    buscar_tigo_en_bd()
    
    print(f"\n🎯 SOLUCIONES:")
    print("1. Si TIGO no existe → Usar otro cliente para comparación")
    print("2. Si es 'TIGO PARAGUAY' → Actualizar aliases")
    print("3. Si es otro nombre → Agregar al sistema de identificación")

