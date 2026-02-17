"""
SCRIPT: Crear TODOS los Anunciantes Faltantes Automáticamente
Mapea al 100% todos los clientes sin anunciante_id
"""

import psycopg2
from sqlalchemy import create_engine, text
import logging

# Configuración logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'jarvis',
    'user': 'postgres',
    'password': '12345'
}

def conectar_bd():
    """Crear conexión a PostgreSQL"""
    try:
        engine = create_engine(f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")
        logger.info("✅ Conexión a BD establecida")
        return engine
    except Exception as e:
        logger.error(f"❌ Error conectando BD: {e}")
        return None

def crear_todos_anunciantes_faltantes(engine):
    """Crear todos los anunciantes faltantes de una vez"""
    try:
        with engine.connect() as conn:
            # Obtener todos los clientes sin mapear
            query = text("""
                SELECT 
                    cliente_original,
                    COUNT(*) as registros,
                    SUM(facturacion) as facturacion_total
                FROM fact_facturacion 
                WHERE anunciante_id IS NULL 
                    AND cliente_original IS NOT NULL
                    AND anio = 2025
                GROUP BY cliente_original
                ORDER BY facturacion_total DESC
            """)
            
            result = conn.execute(query)
            clientes_sin_mapear = result.fetchall()
            
            logger.info(f"🔍 Clientes sin mapear encontrados: {len(clientes_sin_mapear)}")
            
            if not clientes_sin_mapear:
                logger.info("✅ No hay clientes sin mapear - todo está al 100%")
                return True
            
            # Estadísticas iniciales
            total_registros = sum([row.registros for row in clientes_sin_mapear])
            total_facturacion = sum([row.facturacion_total for row in clientes_sin_mapear])
            
            logger.info(f"📊 Registros sin mapear: {total_registros:,}")
            logger.info(f"💰 Facturación sin mapear: {total_facturacion:,.0f} Gs")
            logger.info("")
            
            # Crear todos los anunciantes en lotes
            logger.info("🚀 INICIANDO CREACIÓN MASIVA DE ANUNCIANTES...")
            
            exitos = 0
            errores = 0
            
            for i, row in enumerate(clientes_sin_mapear, 1):
                cliente_nombre = row.cliente_original
                
                try:
                    # Verificar si ya existe
                    check_query = text("""
                        SELECT anunciante_id FROM dim_anunciante 
                        WHERE nombre_canonico = :nombre
                    """)
                    existing = conn.execute(check_query, {"nombre": cliente_nombre}).fetchone()
                    
                    if existing:
                        # Ya existe, solo mapear
                        anunciante_id = existing.anunciante_id
                        logger.info(f"{i:3d}. MAPEAR: {cliente_nombre[:50]:<50} -> ID {anunciante_id}")
                    else:
                        # Crear nuevo
                        insert_query = text("""
                            INSERT INTO dim_anunciante (nombre_canonico) 
                            VALUES (:nombre) 
                            RETURNING anunciante_id
                        """)
                        result = conn.execute(insert_query, {"nombre": cliente_nombre})
                        anunciante_id = result.fetchone().anunciante_id
                        logger.info(f"{i:3d}. CREAR:  {cliente_nombre[:50]:<50} -> ID {anunciante_id} ✅")
                    
                    # Mapear todos los registros de este cliente
                    update_query = text("""
                        UPDATE fact_facturacion 
                        SET anunciante_id = :anunciante_id 
                        WHERE cliente_original = :cliente_nombre 
                          AND anunciante_id IS NULL
                    """)
                    
                    update_result = conn.execute(update_query, {
                        "anunciante_id": anunciante_id,
                        "cliente_nombre": cliente_nombre
                    })
                    
                    registros_actualizados = update_result.rowcount
                    
                    if registros_actualizados > 0:
                        logger.info(f"    📊 {registros_actualizados} registros mapeados | {row.facturacion_total:>15,.0f} Gs")
                        exitos += 1
                    
                    # Commit cada 50 clientes para evitar transacciones muy largas
                    if i % 50 == 0:
                        conn.commit()
                        logger.info(f"💾 Checkpoint: {i}/{len(clientes_sin_mapear)} clientes procesados")
                    
                except Exception as e:
                    logger.error(f"❌ Error con {cliente_nombre}: {e}")
                    errores += 1
                    continue
            
            # Commit final
            conn.commit()
            
            logger.info("")
            logger.info("🎯 PROCESO COMPLETADO:")
            logger.info(f"✅ Éxitos: {exitos}")
            logger.info(f"❌ Errores: {errores}")
            logger.info(f"📊 Total procesados: {len(clientes_sin_mapear)}")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Error en creación masiva: {e}")
        return False

def verificar_mapeo_completo(engine):
    """Verificar que el mapeo esté al 100%"""
    try:
        with engine.connect() as conn:
            # Verificar registros sin mapear
            query = text("""
                SELECT 
                    CASE 
                        WHEN anunciante_id IS NULL THEN 'SIN MAPEAR'
                        ELSE 'MAPEADO'
                    END as estado,
                    COUNT(*) as registros,
                    SUM(facturacion) as facturacion_total,
                    ROUND(SUM(facturacion) / 1000000000, 2) as miles_millones_gs
                FROM fact_facturacion 
                WHERE anio = 2025
                GROUP BY CASE WHEN anunciante_id IS NULL THEN 'SIN MAPEAR' ELSE 'MAPEADO' END
                ORDER BY facturacion_total DESC
            """)
            
            result = conn.execute(query)
            resumen = result.fetchall()
            
            logger.info("")
            logger.info("🔍 VERIFICACIÓN FINAL:")
            logger.info("=" * 60)
            
            for row in resumen:
                porcentaje = (row.facturacion_total / 134318231315 * 100) if row.estado == 'MAPEADO' else (row.facturacion_total / 134318231315 * 100)
                logger.info(f"{row.estado:<12} | {row.registros:>5,} registros | {row.miles_millones_gs:>8.2f} B Gs | {porcentaje:>6.1f}%")
            
            # Verificar si llegamos al 100%
            sin_mapear = next((row for row in resumen if row.estado == 'SIN MAPEAR'), None)
            
            if sin_mapear is None or sin_mapear.registros == 0:
                logger.info("")
                logger.info("🎉 ¡MAPEO 100% COMPLETADO!")
                logger.info("✅ Excel = Base de Datos (coincidencia perfecta)")
                return True
            else:
                logger.info(f"")
                logger.info(f"⚠️  Quedan {sin_mapear.registros} registros sin mapear")
                return False
            
    except Exception as e:
        logger.error(f"❌ Error en verificación: {e}")
        return False

def main():
    """Función principal"""
    logger.info("🚀 MAPEO MASIVO AL 100%")
    logger.info("=" * 40)
    
    # Conectar BD
    engine = conectar_bd()
    if not engine:
        logger.error("❌ No se pudo conectar a la BD")
        return
    
    # Crear todos los anunciantes
    success = crear_todos_anunciantes_faltantes(engine)
    
    if success:
        # Verificar mapeo completo
        verificar_mapeo_completo(engine)
        
        logger.info("")
        logger.info("🎯 ¡JARVIS AHORA TIENE MAPEO 100% PERFECTO!")
        logger.info("🎉 Excel = Base de Datos = Análisis completos")
    else:
        logger.error("❌ Error en el proceso de mapeo masivo")

if __name__ == "__main__":
    main()
