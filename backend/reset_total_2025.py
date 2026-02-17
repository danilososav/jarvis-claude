"""
RESET TOTAL: Eliminar todo 2025 y recargar desde Excel con 100% precisión
"""

import pandas as pd
from sqlalchemy import create_engine, text
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BD
engine = create_engine("postgresql://postgres:123@localhost/jarvis")

def reset_total_2025():
    """Eliminación total y recarga desde cero"""
    
    logger.info("🔥 RESET TOTAL - ELIMINACIÓN Y RECARGA COMPLETA")
    logger.info("=" * 60)
    
    # 1. ELIMINAR TODO 2025 DE LA BD
    with engine.connect() as conn:
        # Backup primero
        backup_query = text("""
            CREATE TABLE IF NOT EXISTS fact_facturacion_backup_reset AS 
            SELECT * FROM fact_facturacion WHERE anio = 2025
        """)
        conn.execute(backup_query)
        
        # Eliminar TODO 2025
        delete_query = text("DELETE FROM fact_facturacion WHERE anio = 2025")
        result = conn.execute(delete_query)
        deleted_count = result.rowcount
        conn.commit()
        
        logger.info(f"🗑️ Registros 2025 eliminados: {deleted_count:,}")
    
    # 2. LEER EXCEL FRESCO
    logger.info("📊 Leyendo Excel BASE_2025.xlsx...")
    
    df = pd.read_excel('BASE_2025.xlsx')
    
    # Procesar datos con máxima precisión
    df['FACTURACION'] = pd.to_numeric(df['FACTURACION'], errors='coerce').fillna(0)
    df['COSTO'] = pd.to_numeric(df['COSTO'], errors='coerce').fillna(0)
    df['REVENUE'] = pd.to_numeric(df['REVENUE'], errors='coerce').fillna(0)
    df['FECHA DE FACT.'] = pd.to_datetime(df['FECHA DE FACT.'], errors='coerce')
    df['anio'] = df['FECHA DE FACT.'].dt.year
    df['mes'] = df['FECHA DE FACT.'].dt.month
    
    # Solo 2025
    df_2025 = df[df['anio'] == 2025].copy()
    
    logger.info(f"📈 Excel registros 2025: {len(df_2025):,}")
    logger.info(f"💰 Excel facturación total: {df_2025['FACTURACION'].sum():,.2f} Gs")
    
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
    
    df_2025 = df_2025.rename(columns=column_mapping)
    df_2025['created_at'] = pd.Timestamp.now()
    
    # 3. MAPEAR CLIENTES (reutilizar mapeo existente)
    logger.info("🔗 Mapeando clientes...")
    
    with engine.connect() as conn:
        # Obtener mapeos existentes
        anunciantes_query = text("SELECT anunciante_id, nombre_canonico FROM dim_anunciante")
        anunciantes_df = pd.read_sql(anunciantes_query, conn)
    
    def mapear_cliente(cliente_nombre):
        if pd.isna(cliente_nombre):
            return None
        
        # Buscar coincidencia exacta en nombre_canonico
        match = anunciantes_df[anunciantes_df['nombre_canonico'] == str(cliente_nombre)]
        if not match.empty:
            return match.iloc[0]['anunciante_id']
        
        return None
    
    df_2025['anunciante_id'] = df_2025['cliente_original'].apply(mapear_cliente)
    df_2025['anunciante_id'] = df_2025['anunciante_id'].astype('Int64')  # Permite NULL
    
    # 4. INSERTAR EN BD
    logger.info("📥 Insertando datos frescos...")
    
    with engine.connect() as conn:
        # Insertar en lotes
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(df_2025), batch_size):
            batch = df_2025.iloc[i:i+batch_size]
            batch.to_sql('fact_facturacion', conn, if_exists='append', index=False, method='multi')
            total_inserted += len(batch)
            
            if i % 5000 == 0:
                logger.info(f"📥 Insertados: {total_inserted:,}/{len(df_2025):,}")
        
        conn.commit()
        logger.info(f"✅ Total insertado: {total_inserted:,} registros")
        
        # 5. VERIFICACIÓN FINAL
        verify_query = text("""
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
        
        verification = conn.execute(verify_query).fetchall()
        
        logger.info("")
        logger.info("🎯 VERIFICACIÓN FINAL:")
        for row in verification:
            logger.info(f"   {row.cliente_original}")
            logger.info(f"   Registros: {row.registros:,}")
            logger.info(f"   Facturación: {float(row.facturacion_total):,.0f} Gs")
        
        # Total general
        total_query = text("SELECT COUNT(*), SUM(facturacion) FROM fact_facturacion WHERE anio = 2025")
        total_result = conn.execute(total_query).fetchone()
        
        logger.info("")
        logger.info(f"📊 TOTAL BD: {total_result[0]:,} registros, {float(total_result[1]):,.2f} Gs")
        logger.info(f"📊 TOTAL EXCEL: {len(df_2025):,} registros, {df_2025['FACTURACION'].sum():,.2f} Gs")
        
        diff_registros = len(df_2025) - total_result[0] 
        diff_facturacion = df_2025['FACTURACION'].sum() - float(total_result[1])
        
        logger.info(f"📊 DIFERENCIA: {diff_registros} registros, {diff_facturacion:.2f} Gs")
        
        if abs(diff_registros) == 0 and abs(diff_facturacion) < 1:
            logger.info("")
            logger.info("🎉 ¡RESET COMPLETADO CON ÉXITO!")
            logger.info("✅ Excel y BD coinciden EXACTAMENTE")
            logger.info("✅ JARVIS ahora tendrá números perfectos")
        else:
            logger.warning("⚠️ Aún hay diferencias menores")

if __name__ == "__main__":
    reset_total_2025()
