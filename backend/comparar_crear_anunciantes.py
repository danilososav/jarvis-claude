"""
SCRIPT: Comparar y Crear Anunciantes Inteligente
Compara anunciantes faltantes con existentes para detectar duplicados y crear solo los necesarios
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
    nombre = re.sub(r'\bS\.?A\.?C\.?I\.?\b', 'SACI', nombre)
    nombre = re.sub(r'\bLTDA\.?\b', 'LTDA', nombre)
    
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

def comparar_anunciantes(engine):
    """Comparar anunciantes faltantes con existentes"""
    try:
        with engine.connect() as conn:
            # Obtener anunciantes existentes
            existing_query = text("""
                SELECT anunciante_id, nombre_anunciante 
                FROM dim_anunciante_perfil 
                ORDER BY anunciante_id
            """)
            existing_df = pd.read_sql(existing_query, conn)
            
            # Obtener anunciantes faltantes
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
            """)
            missing_df = pd.read_sql(missing_query, conn)
            
            logger.info(f"📋 Anunciantes existentes: {len(existing_df)}")
            logger.info(f"🔍 Anunciantes faltantes: {len(missing_df)}")
            logger.info("="*80)
            
            # Análisis de similitudes
            resultados = []
            
            for _, missing_row in missing_df.iterrows():
                cliente_faltante = missing_row['cliente_original']
                mejor_match = None
                mejor_similitud = 0
                
                # Buscar el mejor match
                for _, existing_row in existing_df.iterrows():
                    similitud = similitud_nombres(cliente_faltante, existing_row['nombre_anunciante'])
                    
                    if similitud > mejor_similitud:
                        mejor_similitud = similitud
                        mejor_match = existing_row
                
                # Clasificar resultado
                if mejor_similitud >= 0.85:  # Muy similar, probablemente duplicado
                    accion = "DUPLICADO_PROBABLE"
                elif mejor_similitud >= 0.70:  # Similar, revisar manualmente
                    accion = "REVISAR_MANUAL"
                else:  # Completamente nuevo
                    accion = "CREAR_NUEVO"
                
                resultados.append({
                    'cliente_faltante': cliente_faltante,
                    'registros': int(missing_row['registros']),
                    'facturacion': float(missing_row['facturacion_total']),
                    'mejor_match': mejor_match['nombre_anunciante'] if mejor_match is not None else None,
                    'anunciante_id_match': int(mejor_match['anunciante_id']) if mejor_match is not None else None,
                    'similitud': float(mejor_similitud),
                    'accion': accion
                })
            
            # Crear DataFrame con resultados
            results_df = pd.DataFrame(resultados)
            
            # Mostrar estadísticas
            logger.info("📊 RESUMEN DE COMPARACIÓN:")
            logger.info(f"🔄 Duplicados probables (≥85%): {len(results_df[results_df['accion'] == 'DUPLICADO_PROBABLE'])}")
            logger.info(f"🤔 Revisar manual (70-84%): {len(results_df[results_df['accion'] == 'REVISAR_MANUAL'])}")
            logger.info(f"🆕 Crear nuevos (<70%): {len(results_df[results_df['accion'] == 'CREAR_NUEVO'])}")
            logger.info("")
            
            # Mostrar duplicados probables
            duplicados = results_df[results_df['accion'] == 'DUPLICADO_PROBABLE'].sort_values('facturacion', ascending=False)
            if len(duplicados) > 0:
                logger.info("🔄 DUPLICADOS PROBABLES (Top 20):")
                logger.info("-" * 120)
                logger.info(f"{'CLIENTE FALTANTE':<45} {'MATCH EXISTENTE':<45} {'SIMILITUD':<10} {'FACTURACIÓN'}")
                logger.info("-" * 120)
                
                for _, row in duplicados.head(20).iterrows():
                    logger.info(f"{row['cliente_faltante'][:44]:<45} {str(row['mejor_match'])[:44]:<45} {row['similitud']:.0%}        {row['facturacion']:>15,.0f}")
                logger.info("")
            
            # Mostrar casos para revisión manual
            revisar = results_df[results_df['accion'] == 'REVISAR_MANUAL'].sort_values('facturacion', ascending=False)
            if len(revisar) > 0:
                logger.info("🤔 REVISAR MANUALMENTE (Top 15):")
                logger.info("-" * 120)
                logger.info(f"{'CLIENTE FALTANTE':<45} {'MATCH EXISTENTE':<45} {'SIMILITUD':<10} {'FACTURACIÓN'}")
                logger.info("-" * 120)
                
                for _, row in revisar.head(15).iterrows():
                    logger.info(f"{row['cliente_faltante'][:44]:<45} {str(row['mejor_match'])[:44]:<45} {row['similitud']:.0%}        {row['facturacion']:>15,.0f}")
                logger.info("")
            
            # Mostrar nuevos a crear (Top 30 por facturación)
            nuevos = results_df[results_df['accion'] == 'CREAR_NUEVO'].sort_values('facturacion', ascending=False)
            if len(nuevos) > 0:
                logger.info("🆕 NUEVOS ANUNCIANTES A CREAR (Top 30):")
                logger.info("-" * 100)
                logger.info(f"{'#':<3} {'CLIENTE':<55} {'REGISTROS':<10} {'FACTURACIÓN (Gs)'}")
                logger.info("-" * 100)
                
                for i, (_, row) in enumerate(nuevos.head(30).iterrows(), 1):
                    logger.info(f"{i:<3} {row['cliente_faltante'][:54]:<55} {row['registros']:<10} {row['facturacion']:>15,.0f}")
            
            # Exportar resultados detallados
            results_df.to_csv('comparacion_anunciantes.csv', index=False)
            logger.info(f"")
            logger.info(f"📄 Análisis completo exportado a: comparacion_anunciantes.csv")
            
            return results_df
            
    except Exception as e:
        logger.error(f"❌ Error en comparación: {e}")
        return None

def generar_script_actualizacion(results_df):
    """Generar scripts SQL para actualizar duplicados y crear nuevos"""
    if results_df is None:
        return
    
    try:
        # Script para actualizar duplicados
        duplicados = results_df[results_df['accion'] == 'DUPLICADO_PROBABLE']
        if len(duplicados) > 0:
            with open('actualizar_duplicados.sql', 'w', encoding='utf-8') as f:
                f.write("-- ACTUALIZAR CLIENTES DUPLICADOS\n")
                f.write("-- Mapear clientes faltantes a anunciantes existentes\n\n")
                
                for _, row in duplicados.iterrows():
                    cliente_escaped = row['cliente_faltante'].replace("'", "''")
                    f.write(f"-- {row['cliente_faltante']} -> {row['mejor_match']} (ID: {row['anunciante_id_match']})\n")
                    f.write(f"UPDATE fact_facturacion \n")
                    f.write(f"SET anunciante_id = {row['anunciante_id_match']} \n")
                    f.write(f"WHERE cliente_original = '{cliente_escaped}';\n\n")
            
            logger.info(f"📝 Script de duplicados generado: actualizar_duplicados.sql")
        
        # Script para crear nuevos anunciantes
        nuevos = results_df[results_df['accion'] == 'CREAR_NUEVO'].sort_values('facturacion', ascending=False)
        if len(nuevos) > 0:
            with open('crear_anunciantes_nuevos.sql', 'w', encoding='utf-8') as f:
                f.write("-- CREAR NUEVOS ANUNCIANTES\n")
                f.write("-- Insertar anunciantes completamente nuevos\n\n")
                
                # Obtener el próximo anunciante_id disponible
                next_id = 1000  # Empezar desde 1000 para evitar conflictos
                
                for _, row in nuevos.iterrows():
                    cliente_escaped = row['cliente_faltante'].replace("'", "''")
                    f.write(f"-- {row['cliente_faltante']} - {row['facturacion']:,.0f} Gs ({row['registros']} registros)\n")
                    f.write(f"INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) \n")
                    f.write(f"VALUES ({next_id}, '{cliente_escaped}');\n")
                    f.write(f"UPDATE fact_facturacion \n")
                    f.write(f"SET anunciante_id = {next_id} \n")
                    f.write(f"WHERE cliente_original = '{cliente_escaped}';\n\n")
                    
                    next_id += 1
            
            logger.info(f"📝 Script de nuevos generado: crear_anunciantes_nuevos.sql")
        
    except Exception as e:
        logger.error(f"❌ Error generando scripts: {e}")

def main():
    """Función principal"""
    logger.info("🔍 COMPARANDO ANUNCIANTES FALTANTES VS EXISTENTES")
    logger.info("=" * 60)
    
    # Conectar BD
    engine = conectar_bd()
    if not engine:
        logger.error("❌ No se pudo conectar a la BD")
        return
    
    # Comparar anunciantes
    results_df = comparar_anunciantes(engine)
    
    # Generar scripts de actualización
    generar_script_actualizacion(results_df)
    
    if results_df is not None:
        logger.info("")
        logger.info("🎯 PRÓXIMOS PASOS:")
        logger.info("1. Revisar 'comparacion_anunciantes.csv' para análisis detallado")
        logger.info("2. Ejecutar 'actualizar_duplicados.sql' para mapear duplicados")
        logger.info("3. Revisar casos manuales antes de ejecutar")
        logger.info("4. Ejecutar 'crear_anunciantes_nuevos.sql' para crear nuevos")
        logger.info("5. ¡JARVIS tendrá mapeo 100% completo!")
    else:
        logger.error("❌ Error en el proceso")

if __name__ == "__main__":
    main()