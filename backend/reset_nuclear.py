"""
RESET NUCLEAR - Eliminar TODO y recargar solo Excel actual
"""

import pandas as pd
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine("postgresql://postgres:123@localhost/jarvis")

def reset_nuclear():
    """Reset nuclear - limpiar todo y cargar fresco"""
    
    logger.info("💥 RESET NUCLEAR - ELIMINACIÓN TOTAL")
    logger.info("=" * 50)
    
    with engine.connect() as conn:
        # 1. ELIMINAR ABSOLUTAMENTE TODO
        logger.info("🗑️ Eliminando TODO de fact_facturacion...")
        delete_all = text("TRUNCATE TABLE fact_facturacion CASCADE")
        conn.execute(delete_all)
        conn.commit()
        
        # Verificar que esté vacío
        count = conn.execute(text("SELECT COUNT(*) FROM fact_facturacion")).fetchone()[0]
        logger.info(f"✅ BD vacía: {count} registros")
    
    # 2. LEER EXCEL ACTUAL
    logger.info("📊 Leyendo Excel BASE_2025.xlsx...")
    df = pd.read_excel('BASE_2025.xlsx')
    
    # Mostrar info básica
    logger.info(f"📈 Excel total: {len(df):,} filas")
    
    # Procesar fechas y filtrar
    df['FACTURACION'] = pd.to_numeric(df['FACTURACION'], errors='coerce').fillna(0)
    df['COSTO'] = pd.to_numeric(df['COSTO'], errors='coerce').fillna(0)
    df['REVENUE'] = pd.to_numeric(df['REVENUE'], errors='coerce').fillna(0)
    df['FECHA DE FACT.'] = pd.to_datetime(df['FECHA DE FACT.'], errors='coerce')
    df['anio'] = df['FECHA DE FACT.'].dt.year
    df['mes'] = df['FECHA DE FACT.'].dt.month
    
    # SOLO 2025
    df_2025 = df[df['anio'] == 2025].copy()
    logger.info(f"📈 Solo 2025: {len(df_2025):,} registros")
    logger.info(f"💰 Facturación: {df_2025['FACTURACION'].sum():,.2f} Gs")
    
    # Verificar top 2 del Excel
    top_excel = df_2025.groupby('CLIENTE')['FACTURACION'].agg(['count', 'sum']).sort_values('sum', ascending=False).head(2)
    logger.info("🏆 Top 2 Excel:")
    for cliente, data in top_excel.iterrows():
        logger.info(f"   {cliente}: {data['count']} reg, {data['sum']:,.0f} Gs")
    
    # 3. PREPARAR DATOS PARA BD
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
    
    df_final = df_2025.copy()
    for excel_col, db_col in column_mapping.items():
        if excel_col in df_final.columns:
            df_final = df_final.rename(columns={excel_col: db_col})
    
    df_final['created_at'] = pd.Timestamp.now()
    df_final['anunciante_id'] = None  # Lo mapearemos después
    
    # 4. INSERTAR EN BD
    with engine.connect() as conn:
        logger.info("📥 Insertando datos frescos...")
        df_final.to_sql('fact_facturacion', conn, if_exists='append', index=False, method='multi')
        conn.commit()
        
        logger.info(f"✅ Insertados: {len(df_final):,} registros")
        
        # 5. VERIFICAR INMEDIATAMENTE
        verify_query = text("""
            SELECT 
                cliente_original,
                COUNT(*) as registros,
                SUM(facturacion) as total
            FROM fact_facturacion 
            WHERE cliente_original IN ('CERVEPAR S.A.', 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.')
            GROUP BY cliente_original
            ORDER BY total DESC
        """)
        
        result = conn.execute(verify_query).fetchall()
        
        logger.info("🎯 VERIFICACIÓN INMEDIATA:")
        for row in result:
            logger.info(f"   {row.cliente_original}: {row.registros} reg, {float(row.total):,.0f} Gs")
        
        # Verificar total
        total_check = conn.execute(text("SELECT COUNT(*), SUM(facturacion) FROM fact_facturacion")).fetchone()
        logger.info(f"📊 TOTAL BD: {total_check[0]:,} reg, {float(total_check[1]):,.0f} Gs")
        
        if len(result) >= 2:
            cervepar_correcto = abs(float(result[0].total) - 26057164652) < 1000
            telefonica_correcto = abs(float(result[1].total) - 9213656412) < 1000
            
            if cervepar_correcto and telefonica_correcto:
                logger.info("🎉 ¡NÚMEROS CORRECTOS!")
            else:
                logger.error("❌ Números aún incorrectos")

if __name__ == "__main__":
    reset_nuclear()
