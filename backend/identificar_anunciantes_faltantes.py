"""
SCRIPT: Identificar Anunciantes Faltantes
Después de cargar todos los datos, identificar qué clientes necesitan crearse en dim_anunciante_perfil
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
    'password': '12345'  # Usar la misma config que en el otro script
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

def identificar_anunciantes_faltantes(engine):
    """Identificar clientes sin anunciante_id que necesitan ser creados"""
    try:
        with engine.connect() as conn:
            # Obtener clientes sin mapear (anunciante_id es NULL)
            query = text("""
                SELECT 
                    cliente_original,
                    COUNT(*) as registros,
                    SUM(facturacion) as facturacion_total,
                    MIN(fecha_fact) as primera_factura,
                    MAX(fecha_fact) as ultima_factura
                FROM fact_facturacion 
                WHERE anunciante_id IS NULL 
                    AND cliente_original IS NOT NULL
                GROUP BY cliente_original
                ORDER BY facturacion_total DESC
            """)
            
            result = conn.execute(query)
            faltantes = result.fetchall()
            
            if not faltantes:
                logger.info("✅ No hay anunciantes faltantes - todos están mapeados")
                return
            
            logger.info(f"🔍 ANUNCIANTES FALTANTES: {len(faltantes)}")
            logger.info("="*80)
            
            # Estadísticas generales
            total_registros = sum([row.registros for row in faltantes])
            total_facturacion = sum([row.facturacion_total for row in faltantes])
            
            logger.info(f"📊 Total registros sin mapear: {total_registros:,}")
            logger.info(f"💰 Total facturación perdida: {total_facturacion:,.0f} Gs")
            logger.info("")
            
            # Top 50 por facturación
            logger.info("🏆 TOP 50 ANUNCIANTES FALTANTES (por facturación):")
            logger.info("-" * 100)
            logger.info(f"{'#':<3} {'CLIENTE':<50} {'REGISTROS':<10} {'FACTURACIÓN (Gs)':<20} {'PERÍODO'}")
            logger.info("-" * 100)
            
            for i, row in enumerate(faltantes[:50], 1):
                periodo = f"{row.primera_factura.strftime('%Y-%m')} - {row.ultima_factura.strftime('%Y-%m')}"
                logger.info(f"{i:<3} {row.cliente_original[:50]:<50} {row.registros:<10} {row.facturacion_total:>18,.0f} {periodo}")
            
            # Exportar a CSV para revisión
            df_faltantes = pd.DataFrame([
                {
                    'cliente_original': row.cliente_original,
                    'registros': row.registros, 
                    'facturacion_total': float(row.facturacion_total),
                    'primera_factura': row.primera_factura,
                    'ultima_factura': row.ultima_factura
                } for row in faltantes
            ])
            
            csv_filename = "anunciantes_faltantes.csv"
            df_faltantes.to_csv(csv_filename, index=False)
            logger.info(f"")
            logger.info(f"📄 Lista completa exportada a: {csv_filename}")
            
            # Análisis adicional
            logger.info("")
            logger.info("🔍 ANÁLISIS ADICIONAL:")
            logger.info(f"• Clientes con >1000 registros: {len([r for r in faltantes if r.registros > 1000])}")
            logger.info(f"• Clientes con >1M Gs: {len([r for r in faltantes if r.facturacion_total > 1000000])}")
            logger.info(f"• Clientes con >1B Gs: {len([r for r in faltantes if r.facturacion_total > 1000000000])}")
            
            # Sugerencias de nombres más comunes
            logger.info("")
            logger.info("💡 PATRONES DETECTADOS:")
            
            # Buscar patrones comunes
            patterns = {}
            for row in faltantes:
                nombre = row.cliente_original.upper()
                if 'S.A.' in nombre:
                    patterns['Sociedades Anónimas'] = patterns.get('Sociedades Anónimas', 0) + 1
                if 'S.R.L.' in nombre:
                    patterns['Sociedades de Responsabilidad Limitada'] = patterns.get('Sociedades de Responsabilidad Limitada', 0) + 1
                if 'BANCO' in nombre:
                    patterns['Bancos'] = patterns.get('Bancos', 0) + 1
                if 'FARMACIA' in nombre or 'LABORATORIO' in nombre:
                    patterns['Farmacéuticas'] = patterns.get('Farmacéuticas', 0) + 1
                if any(word in nombre for word in ['SUPERMERCADO', 'COMERCIAL', 'DISTRIBUIDORA']):
                    patterns['Retail/Distribución'] = patterns.get('Retail/Distribución', 0) + 1
            
            for pattern, count in patterns.items():
                logger.info(f"• {pattern}: {count} empresas")
            
            return df_faltantes
            
    except Exception as e:
        logger.error(f"❌ Error identificando faltantes: {e}")
        return None

def main():
    """Función principal"""
    logger.info("🔍 IDENTIFICANDO ANUNCIANTES FALTANTES")
    logger.info("=" * 50)
    
    # Conectar BD
    engine = conectar_bd()
    if not engine:
        logger.error("❌ No se pudo conectar a la BD")
        return
    
    # Identificar faltantes
    df_faltantes = identificar_anunciantes_faltantes(engine)
    
    if df_faltantes is not None:
        logger.info("")
        logger.info("🎯 PRÓXIMOS PASOS:")
        logger.info("1. Revisar archivo 'anunciantes_faltantes.csv'")
        logger.info("2. Crear script para insertar nuevos anunciantes")
        logger.info("3. Actualizar anunciante_id en fact_facturacion")
        logger.info("4. ¡JARVIS tendrá análisis 100% completos!")
    else:
        logger.error("❌ Error en el proceso")

if __name__ == "__main__":
    main()
