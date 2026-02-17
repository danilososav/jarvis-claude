"""
CARGA FINAL: Planilla Excel corregida solo con 2025
"""

import pandas as pd
from sqlalchemy import create_engine, text
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BD
engine = create_engine("postgresql://postgres:123@localhost/jarvis")

def carga_final_2025():
    """Carga final con Excel corregido"""
    
    logger.info("🔥 CARGA FINAL - EXCEL CORREGIDO 2025")
    logger.info("=" * 50)
    
    # 1. LEER EXCEL CORREGIDO desde backend
    logger.info("📊 Leyendo Excel corregido...")
    
    try:
        df = pd.read_excel('BASE_2025.xlsx')
        logger.info(f"📈 Total filas Excel: {len(df):,}")
    except Exception as e:
        logger.error(f"❌ Error leyendo Excel: {e}")
        return
    
    # Mostrar primeras filas para verificar
    logger.info("🔍 Primeras 5 filas del Excel:")
    print(df.head())
    print("\n📋 Columnas disponibles:")
    print(df.columns.tolist())
    
    # Procesar datos
    if 'FACTURACION' in df.columns:
        df['FACTURACION'] = pd.to_numeric(df['FACTURACION'], errors='coerce').fillna(0)
    if 'COSTO' in df.columns:
        df['COSTO'] = pd.to_numeric(df['COSTO'], errors='coerce').fillna(0)
    if 'REVENUE' in df.columns:
        df['REVENUE'] = pd.to_numeric(df['REVENUE'], errors='coerce').fillna(0)
    
    # Verificar fechas
    if 'FECHA DE FACT.' in df.columns:
        df['FECHA DE FACT.'] = pd.to_datetime(df['FECHA DE FACT.'], errors='coerce')
        df['anio'] = df['FECHA DE FACT.'].dt.year
        df['mes'] = df['FECHA DE FACT.'].dt.month
        
        # Ver qué años hay
        years_in_excel = df['anio'].value_counts().sort_index()
        logger.info("📊 Años en Excel:")
        for year, count in years_in_excel.items():
            logger.info(f"   {year}: {count:,} registros")
        
        # Filtrar solo 2025
        df_2025 = df[df['anio'] == 2025].copy()
        logger.info(f"📈 Registros 2025: {len(df_2025):,}")
        logger.info(f"💰 Facturación 2025: {df_2025['FACTURACION'].sum():,.2f} Gs")
        
        # Top 3 para verificar
        if 'CLIENTE' in df_2025.columns:
            top_3 = df_2025.groupby('CLIENTE')['FACTURACION'].agg(['count', 'sum']).sort_values('sum', ascending=False).head(3)
            logger.info("🏆 Top 3 Excel:")
            for cliente, data in top_3.iterrows():
                logger.info(f"   {cliente}: {data['count']} reg, {data['sum']:,.0f} Gs")
    
    # 2. ELIMINAR TODO DE LA BD Y CARGAR FRESCO
    with engine.connect() as conn:
        logger.info("🗑️ Eliminando datos anteriores...")
        delete_all = text("DELETE FROM fact_facturacion")
        result = conn.execute(delete_all)
        deleted = result.rowcount
        logger.info(f"🗑️ Eliminados: {deleted:,} registros")
        
        logger.info("📥 Preparando datos para insertar...")
        
        # Mapeo de columnas
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
        
        # Renombrar columnas que existen
        df_rename = df_2025.copy()
        for excel_col, db_col in column_mapping.items():
            if excel_col in df_rename.columns:
                df_rename = df_rename.rename(columns={excel_col: db_col})
        
        df_rename['created_at'] = pd.Timestamp.now()
        
        # Mapear clientes
        logger.info("🔗 Mapeando clientes...")
        anunciantes_query = text("SELECT anunciante_id, nombre_canonico FROM dim_anunciante")
        anunciantes_df = pd.read_sql(anunciantes_query, conn)
        
        def mapear_cliente(cliente_nombre):
            if pd.isna(cliente_nombre):
                return None
            match = anunciantes_df[anunciantes_df['nombre_canonico'] == str(cliente_nombre)]
            return match.iloc[0]['anunciante_id'] if not match.empty else None
        
        if 'cliente_original' in df_rename.columns:
            df_rename['anunciante_id'] = df_rename['cliente_original'].apply(mapear_cliente)
            df_rename['anunciante_id'] = df_rename['anunciante_id'].astype('Int64')
        
        # Insertar datos
        logger.info("📥 Insertando datos...")
        df_rename.to_sql('fact_facturacion', conn, if_exists='append', index=False, method='multi')
        conn.commit()
        
        logger.info(f"✅ Insertados: {len(df_rename):,} registros")
        
        # Verificación final
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
        
        logger.info("🎯 VERIFICACIÓN FINAL:")
        for row in verification:
            logger.info(f"   {row.cliente_original}")
            logger.info(f"   Registros: {row.registros:,}")
            logger.info(f"   Facturación: {float(row.facturacion_total):,.0f} Gs")
        
        logger.info("")
        logger.info("🎉 CARGA COMPLETADA")
        logger.info("✅ Datos frescos cargados")

if __name__ == "__main__":
    carga_final_2025()
