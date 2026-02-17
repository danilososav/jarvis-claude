"""
SCRIPT: Debug Comparación Anunciantes
Versión simplificada para encontrar el error exacto
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import logging
from difflib import SequenceMatcher
import re

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

def limpiar_nombre_empresa(nombre):
    """Normalizar nombres de empresas para comparación"""
    if pd.isna(nombre):
        return ""
    
    # Convertir a mayúsculas
    nombre = str(nombre).upper().strip()
    
    # Quitar puntos y comas
    nombre = re.sub(r'[.,]', '', nombre)
    
    # Normalizar tipos societarios
    nombre = re.sub(r'\bS\.?A\.?\b', 'SA', nombre)
    nombre = re.sub(r'\bS\.?R\.?L\.?\b', 'SRL', nombre) 
    nombre = re.sub(r'\bS\.?A\.?E\.?C\.?A\.?\b', 'SAECA', nombre)
    
    # Quitar espacios múltiples
    nombre = re.sub(r'\s+', ' ', nombre).strip()
    
    return nombre

def similitud_nombres(nombre1, nombre2):
    """Calcular similitud entre dos nombres de empresa"""
    nombre1_clean = limpiar_nombre_empresa(nombre1)
    nombre2_clean = limpiar_nombre_empresa(nombre2)
    
    # Similitud exacta
    if nombre1_clean == nombre2_clean:
        return 1.0
    
    # Similitud por secuencia
    return SequenceMatcher(None, nombre1_clean, nombre2_clean).ratio()

def comparar_anunciantes_debug(engine):
    """Comparar anunciantes faltantes con existentes - versión debug"""
    try:
        with engine.connect() as conn:
            # Obtener anunciantes existentes
            logger.info("📋 Obteniendo anunciantes existentes...")
            existing_query = text("""
                SELECT anunciante_id, nombre_anunciante 
                FROM dim_anunciante_perfil 
                ORDER BY anunciante_id
            """)
            existing_df = pd.read_sql(existing_query, conn)
            
            # Obtener solo TOP 5 anunciantes faltantes para debug
            logger.info("🔍 Obteniendo TOP 5 anunciantes faltantes...")
            missing_query = text("""
                SELECT 
                    cliente_original,
                    COUNT(*) as registros,
                    SUM(facturacion) as facturacion_total
                FROM fact_facturacion 
                WHERE anunciante_id IS NULL 
                    AND cliente_original IS NOT NULL
                GROUP BY cliente_original
                ORDER BY facturacion_total DESC
                LIMIT 5
            """)
            missing_df = pd.read_sql(missing_query, conn)
            
            logger.info(f"📋 Anunciantes existentes: {len(existing_df)}")
            logger.info(f"🔍 Anunciantes faltantes (sample): {len(missing_df)}")
            
            # Procesar solo los primeros para debug
            resultados = []
            
            logger.info("🔍 Procesando comparaciones...")
            for idx, missing_row in missing_df.iterrows():
                logger.info(f"Procesando: {missing_row['cliente_original']}")
                
                cliente_faltante = missing_row['cliente_original']
                mejor_match = None
                mejor_similitud = 0
                
                # Buscar el mejor match
                for _, existing_row in existing_df.iterrows():
                    try:
                        similitud = similitud_nombres(cliente_faltante, existing_row['nombre_anunciante'])
                        
                        if similitud > mejor_similitud:
                            mejor_similitud = similitud
                            mejor_match = existing_row
                    except Exception as e:
                        logger.error(f"Error comparando '{cliente_faltante}' con '{existing_row['nombre_anunciante']}': {e}")
                        continue
                
                # Clasificar resultado
                if mejor_similitud >= 0.85:
                    accion = "DUPLICADO_PROBABLE"
                elif mejor_similitud >= 0.70:
                    accion = "REVISAR_MANUAL"
                else:
                    accion = "CREAR_NUEVO"
                
                resultado = {
                    'cliente_faltante': cliente_faltante,
                    'registros': int(missing_row['registros']),
                    'facturacion': float(missing_row['facturacion_total']),
                    'mejor_match': mejor_match['nombre_anunciante'] if mejor_match is not None else None,
                    'anunciante_id_match': int(mejor_match['anunciante_id']) if mejor_match is not None else None,
                    'similitud': float(mejor_similitud),
                    'accion': accion
                }
                
                resultados.append(resultado)
                logger.info(f"✅ {cliente_faltante} -> {accion} (similitud: {mejor_similitud:.2%})")
            
            # Crear DataFrame con resultados
            logger.info("📊 Creando DataFrame...")
            results_df = pd.DataFrame(resultados)
            
            # Mostrar resultados
            logger.info("📋 RESULTADOS:")
            for _, row in results_df.iterrows():
                logger.info(f"• {row['cliente_faltante']} -> {row['accion']} -> {row['mejor_match']} ({row['similitud']:.0%})")
            
            # Guardar CSV
            results_df.to_csv('debug_comparacion.csv', index=False)
            logger.info("✅ Debug completado - archivo: debug_comparacion.csv")
            
            return results_df
            
    except Exception as e:
        logger.error(f"❌ Error en debug: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Función principal"""
    logger.info("🔍 DEBUG: COMPARANDO ANUNCIANTES (TOP 5)")
    logger.info("=" * 50)
    
    # Conectar BD
    engine = conectar_bd()
    if not engine:
        logger.error("❌ No se pudo conectar a la BD")
        return
    
    # Debug comparación
    results_df = comparar_anunciantes_debug(engine)
    
    if results_df is not None:
        logger.info("✅ Debug completado exitosamente")
    else:
        logger.error("❌ Error en el debug")

if __name__ == "__main__":
    main()
