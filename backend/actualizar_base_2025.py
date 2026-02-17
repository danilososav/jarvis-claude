"""
SCRIPT: Actualización BASE_2025.xlsx a PostgreSQL
Actualiza datos de facturación 2025 con archivo completo
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
import numpy as np

# Configuración logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'jarvis',
    'user': 'postgres',
    'password': '12345'  # CAMBIAR
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

def leer_excel_2025(archivo_path):
    """Leer y procesar archivo BASE_2025.xlsx"""
    try:
        logger.info(f"📊 Leyendo archivo: {archivo_path}")
        
        # Leer Excel
        df = pd.read_excel(archivo_path)
        
        logger.info(f"📈 Registros leídos: {len(df):,}")
        logger.info(f"📋 Columnas: {list(df.columns)}")
        
        # Mapeo de columnas Excel → PostgreSQL
        column_mapping = {
            'AGENCIA': 'empresa',
            'UNIDAD DE NEGOCIOS': 'unidad_negocios',
            'REPRESENTADAS': 'representadas', 
            'FAMILIA': 'familia',
            'INTERAGENCIA': 'interagencia',
            'ESTADO': 'estado',
            'FECHA DE FACT.': 'fecha_fact',
            'FACT. N°': 'numero_factura',
            'N° DE PPT': 'numero_ppt',
            'CLIENTE': 'cliente_original',
            'PERIODO DE SERVICIO': 'periodo_servicio',
            'FACTURACION': 'facturacion',
            'COSTO': 'costo', 
            'REVENUE': 'revenue',
            'DIVISION': 'division',
            'ARENA': 'arena',
            'SUB-ARENAS': 'subarenas',
            'DESCRIPCION': 'descripcion'
        }
        
        # Renombrar columnas
        df = df.rename(columns=column_mapping)
        
        # Procesar fechas
        df['fecha_fact'] = pd.to_datetime(df['fecha_fact'], errors='coerce')
        
        # Agregar año y mes
        df['anio'] = df['fecha_fact'].dt.year
        df['mes'] = df['fecha_fact'].dt.month
        
        # Limpiar valores numéricos
        df['facturacion'] = pd.to_numeric(df['facturacion'], errors='coerce').fillna(0)
        df['costo'] = pd.to_numeric(df['costo'], errors='coerce').fillna(0)
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce').fillna(0)
        
        # Filtrar solo 2025 (por seguridad)
        df_2025 = df[df['anio'] == 2025].copy()
        
        logger.info(f"📅 Registros 2025: {len(df_2025):,}")
        logger.info(f"🗓️ Rango fechas: {df_2025['fecha_fact'].min()} - {df_2025['fecha_fact'].max()}")
        
        return df_2025
        
    except Exception as e:
        logger.error(f"❌ Error leyendo Excel: {e}")
        return None

def mapear_clientes_anunciante_id(df, engine):
    """Mapear clientes a anunciante_id de dim_anunciante_perfil"""
    try:
        logger.info("🔗 Mapeando clientes a anunciante_id...")
        
        # Obtener tabla de anunciantes
        with engine.connect() as conn:
            anunciantes_query = text("""
                SELECT anunciante_id, nombre_anunciante 
                FROM dim_anunciante_perfil
            """)
            anunciantes_df = pd.read_sql(anunciantes_query, conn)
        
        logger.info(f"📋 Anunciantes en BD: {len(anunciantes_df)}")
        
        # Función de matching básico
        def encontrar_anunciante_id(cliente_nombre):
            if pd.isna(cliente_nombre):
                return None
                
            cliente_clean = str(cliente_nombre).upper().strip()
            
            # Buscar coincidencia exacta primero
            match = anunciantes_df[anunciantes_df['nombre_anunciante'].str.upper() == cliente_clean]
            if not match.empty:
                return match.iloc[0]['anunciante_id']
            
            # Buscar coincidencia parcial
            for _, row in anunciantes_df.iterrows():
                nombre_bd = row['nombre_anunciante'].upper()
                if cliente_clean in nombre_bd or nombre_bd in cliente_clean:
                    return row['anunciante_id']
            
            return None
        
        # Aplicar mapping
        df['anunciante_id'] = df['cliente_original'].apply(encontrar_anunciante_id)
        
        # Estadísticas de matching
        matched = df['anunciante_id'].notna().sum()
        unmatched = df['anunciante_id'].isna().sum()
        
        logger.info(f"✅ Clientes mapeados: {matched:,} ({matched/len(df)*100:.1f}%)")
        logger.info(f"❌ Sin mapear: {unmatched:,} ({unmatched/len(df)*100:.1f}%)")
        
        if unmatched > 0:
            logger.info("🔍 Clientes sin mapear (muestra):")
            unmapped_sample = df[df['anunciante_id'].isna()]['cliente_original'].unique()[:10]
            for cliente in unmapped_sample:
                logger.info(f"   - {cliente}")
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Error mapeando clientes: {e}")
        return df

def actualizar_base_datos(df, engine):
    """Actualizar base de datos con nuevos datos 2025"""
    try:
        with engine.connect() as conn:
            # 1. Backup de datos existentes 2025
            logger.info("💾 Creando backup de datos 2025 existentes...")
            
            backup_query = text("""
                CREATE TABLE IF NOT EXISTS fact_facturacion_backup_2025 AS 
                SELECT * FROM fact_facturacion WHERE anio = 2025
            """)
            conn.execute(backup_query)
            conn.commit()
            
            # 2. Eliminar datos 2025 existentes
            logger.info("🗑️ Eliminando datos 2025 existentes...")
            
            delete_query = text("DELETE FROM fact_facturacion WHERE anio = 2025")
            result = conn.execute(delete_query)
            deleted_count = result.rowcount
            conn.commit()
            
            logger.info(f"🗑️ Registros eliminados: {deleted_count:,}")
            
            # 3. Insertar nuevos datos
            logger.info("📥 Insertando nuevos datos 2025...")
            
            # Preparar DataFrame para inserción
            df_insert = df.copy()
            
            # INCLUIR TODOS LOS REGISTROS - usar NULL para anunciantes sin mapear
            df_insert['anunciante_id'] = df_insert['anunciante_id'].astype('Int64')  # Permite NULL
            
            # Agregar created_at
            df_insert['created_at'] = datetime.now()
            
            # Insertar en lotes
            batch_size = 1000
            total_inserted = 0
            
            for i in range(0, len(df_insert), batch_size):
                batch = df_insert.iloc[i:i+batch_size]
                batch.to_sql('fact_facturacion', conn, if_exists='append', index=False)
                total_inserted += len(batch)
                
                if i % 5000 == 0:
                    logger.info(f"📥 Insertados: {total_inserted:,}/{len(df_insert):,}")
            
            conn.commit()
            logger.info(f"✅ Total insertado: {total_inserted:,} registros")
            
            # 4. Verificar inserción
            verify_query = text("SELECT COUNT(*) as total FROM fact_facturacion WHERE anio = 2025")
            result = conn.execute(verify_query).fetchone()
            
            logger.info(f"🔍 Verificación - Registros 2025 en BD: {result.total:,}")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Error actualizando BD: {e}")
        return False

def main():
    """Función principal"""
    logger.info("🚀 INICIANDO ACTUALIZACIÓN BASE_2025")
    logger.info("=" * 50)
    
    # 1. Conectar BD
    engine = conectar_bd()
    if not engine:
        logger.error("❌ No se pudo conectar a la BD")
        return
    
    # 2. Leer Excel
    archivo_excel = "BASE_2025.xlsx"  # Ajustar path si es necesario
    df = leer_excel_2025(archivo_excel)
    if df is None:
        logger.error("❌ No se pudo leer el archivo Excel")
        return
    
    # 3. Mapear clientes
    df = mapear_clientes_anunciante_id(df, engine)
    
    # 4. Actualizar BD
    success = actualizar_base_datos(df, engine)
    
    if success:
        logger.info("🎉 ¡ACTUALIZACIÓN COMPLETADA CON ÉXITO!")
        logger.info("✅ Datos 2025 actualizados")
        logger.info("✅ Backup creado")
        logger.info("🚀 JARVIS listo con datos actualizados")
    else:
        logger.error("❌ Error en la actualización")

if __name__ == "__main__":
    main()
