"""
SCRIPT: Verificación Exacta Excel vs Base de Datos
Compara todos los números para confirmar integridad 100%
"""

import pandas as pd
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

def leer_datos_excel():
    """Leer y procesar datos del Excel BASE_2025.xlsx"""
    try:
        logger.info("📊 Leyendo datos del Excel BASE_2025.xlsx...")
        
        # Leer Excel
        df = pd.read_excel('BASE_2025.xlsx')
        
        # Procesar datos
        df['FACTURACION'] = pd.to_numeric(df['FACTURACION'], errors='coerce').fillna(0)
        df['COSTO'] = pd.to_numeric(df['COSTO'], errors='coerce').fillna(0)  
        df['REVENUE'] = pd.to_numeric(df['REVENUE'], errors='coerce').fillna(0)
        df['FECHA DE FACT.'] = pd.to_datetime(df['FECHA DE FACT.'], errors='coerce')
        df['anio'] = df['FECHA DE FACT.'].dt.year
        df['mes'] = df['FECHA DE FACT.'].dt.month
        
        # Filtrar 2025
        df_2025 = df[df['anio'] == 2025].copy()
        
        logger.info(f"📈 Excel - Total registros 2025: {len(df_2025):,}")
        logger.info(f"💰 Excel - Facturación total: {df_2025['FACTURACION'].sum():,.2f} Gs")
        logger.info(f"💵 Excel - Costo total: {df_2025['COSTO'].sum():,.2f} Gs")
        logger.info(f"📊 Excel - Revenue total: {df_2025['REVENUE'].sum():,.2f} Gs")
        
        return df_2025
        
    except Exception as e:
        logger.error(f"❌ Error leyendo Excel: {e}")
        return None

def leer_datos_bd(engine):
    """Leer datos de la Base de Datos"""
    try:
        logger.info("🗄️ Leyendo datos de la Base de Datos...")
        
        with engine.connect() as conn:
            # Consulta principal
            query = text("""
                SELECT 
                    COUNT(*) as total_registros,
                    SUM(facturacion) as facturacion_total,
                    SUM(costo) as costo_total,
                    SUM(revenue) as revenue_total,
                    COUNT(CASE WHEN anunciante_id IS NOT NULL THEN 1 END) as registros_mapeados,
                    COUNT(CASE WHEN anunciante_id IS NULL THEN 1 END) as registros_sin_mapear
                FROM fact_facturacion 
                WHERE anio = 2025
            """)
            
            result = conn.execute(query).fetchone()
            
            logger.info(f"📈 BD - Total registros 2025: {result.total_registros:,}")
            logger.info(f"💰 BD - Facturación total: {float(result.facturacion_total):,.2f} Gs")
            logger.info(f"💵 BD - Costo total: {float(result.costo_total):,.2f} Gs")
            logger.info(f"📊 BD - Revenue total: {float(result.revenue_total):,.2f} Gs")
            logger.info(f"🔗 BD - Registros mapeados: {result.registros_mapeados:,}")
            logger.info(f"❌ BD - Registros sin mapear: {result.registros_sin_mapear:,}")
            
            return result
            
    except Exception as e:
        logger.error(f"❌ Error leyendo BD: {e}")
        return None

def verificar_por_cliente(df_excel, engine):
    """Verificación detallada por cliente"""
    try:
        logger.info("🔍 Verificando facturación por cliente...")
        
        # Agrupar Excel por cliente
        excel_clientes = df_excel.groupby('CLIENTE').agg({
            'FACTURACION': ['count', 'sum'],
            'COSTO': 'sum',
            'REVENUE': 'sum'
        }).round(2)
        
        excel_clientes.columns = ['Registros_Excel', 'Facturacion_Excel', 'Costo_Excel', 'Revenue_Excel']
        excel_clientes = excel_clientes.reset_index()
        
        # Consultar BD por cliente
        with engine.connect() as conn:
            bd_query = text("""
                SELECT 
                    cliente_original as cliente,
                    COUNT(*) as registros_bd,
                    SUM(facturacion) as facturacion_bd,
                    SUM(costo) as costo_bd,
                    SUM(revenue) as revenue_bd
                FROM fact_facturacion 
                WHERE anio = 2025
                    AND cliente_original IS NOT NULL
                GROUP BY cliente_original
                ORDER BY facturacion_bd DESC
            """)
            
            bd_clientes = pd.read_sql(bd_query, conn)
            bd_clientes['facturacion_bd'] = bd_clientes['facturacion_bd'].astype(float).round(2)
            bd_clientes['costo_bd'] = bd_clientes['costo_bd'].astype(float).round(2) 
            bd_clientes['revenue_bd'] = bd_clientes['revenue_bd'].astype(float).round(2)
        
        # Comparar
        comparacion = excel_clientes.merge(
            bd_clientes, 
            left_on='CLIENTE', 
            right_on='cliente',
            how='outer',
            suffixes=('_excel', '_bd')
        )
        
        # Identificar diferencias
        comparacion['diff_registros'] = comparacion['Registros_Excel'].fillna(0) - comparacion['registros_bd'].fillna(0)
        comparacion['diff_facturacion'] = comparacion['Facturacion_Excel'].fillna(0) - comparacion['facturacion_bd'].fillna(0)
        
        # Mostrar top 10 por facturación
        logger.info("")
        logger.info("🏆 TOP 10 CLIENTES - COMPARACIÓN EXCEL vs BD:")
        logger.info("-" * 100)
        logger.info(f"{'CLIENTE':<35} {'EXCEL_FACT':<15} {'BD_FACT':<15} {'DIFERENCIA':<15}")
        logger.info("-" * 100)
        
        for _, row in comparacion.head(10).iterrows():
            cliente = (row['CLIENTE'] if pd.notna(row['CLIENTE']) else row['cliente'])[:34]
            excel_fact = row['Facturacion_Excel'] if pd.notna(row['Facturacion_Excel']) else 0
            bd_fact = row['facturacion_bd'] if pd.notna(row['facturacion_bd']) else 0
            diff = excel_fact - bd_fact
            
            logger.info(f"{cliente:<35} {excel_fact:>13,.0f} {bd_fact:>13,.0f} {diff:>13,.0f}")
        
        # Estadísticas de diferencias
        diferencias_significativas = comparacion[abs(comparacion['diff_facturacion']) > 1].copy()
        
        logger.info("")
        logger.info(f"🔍 Clientes con diferencias significativas: {len(diferencias_significativas)}")
        
        if len(diferencias_significativas) > 0:
            logger.info("⚠️ DIFERENCIAS ENCONTRADAS:")
            for _, row in diferencias_significativas.head(5).iterrows():
                cliente = row['CLIENTE'] if pd.notna(row['CLIENTE']) else row['cliente']
                diff = row['diff_facturacion']
                logger.info(f"   • {cliente}: {diff:,.2f} Gs de diferencia")
        else:
            logger.info("✅ No hay diferencias significativas entre Excel y BD")
        
        return comparacion
        
    except Exception as e:
        logger.error(f"❌ Error en verificación por cliente: {e}")
        return None

def main():
    """Función principal"""
    logger.info("🔍 VERIFICACIÓN EXACTA: EXCEL vs BASE DE DATOS")
    logger.info("=" * 60)
    
    # Conectar BD
    engine = conectar_bd()
    if not engine:
        logger.error("❌ No se pudo conectar a la BD")
        return
    
    # Leer datos Excel
    df_excel = leer_datos_excel()
    if df_excel is None:
        logger.error("❌ No se pudieron leer los datos del Excel")
        return
    
    # Leer datos BD
    bd_data = leer_datos_bd(engine)
    if bd_data is None:
        logger.error("❌ No se pudieron leer los datos de la BD")
        return
    
    logger.info("")
    logger.info("📊 COMPARACIÓN GLOBAL:")
    logger.info("=" * 50)
    
    # Comparar totales
    diff_registros = len(df_excel) - bd_data.total_registros
    diff_facturacion = df_excel['FACTURACION'].sum() - float(bd_data.facturacion_total)
    diff_costo = df_excel['COSTO'].sum() - float(bd_data.costo_total)
    diff_revenue = df_excel['REVENUE'].sum() - float(bd_data.revenue_total)
    
    logger.info(f"📈 Diferencia registros: {diff_registros}")
    logger.info(f"💰 Diferencia facturación: {diff_facturacion:,.2f} Gs")
    logger.info(f"💵 Diferencia costo: {diff_costo:,.2f} Gs")
    logger.info(f"📊 Diferencia revenue: {diff_revenue:,.2f} Gs")
    
    # Determinar resultado
    if abs(diff_registros) == 0 and abs(diff_facturacion) < 1 and abs(diff_costo) < 1 and abs(diff_revenue) < 1:
        logger.info("")
        logger.info("🎉 ¡VERIFICACIÓN EXITOSA!")
        logger.info("✅ Excel y Base de Datos coinciden perfectamente")
        logger.info("✅ Integridad de datos: 100%")
    else:
        logger.info("")
        logger.info("⚠️ Se encontraron diferencias")
        logger.info("🔍 Ejecutando verificación detallada por cliente...")
        
        # Verificación detallada
        comparacion = verificar_por_cliente(df_excel, engine)
    
    logger.info("")
    logger.info("🎯 VERIFICACIÓN COMPLETADA")

if __name__ == "__main__":
    main()
