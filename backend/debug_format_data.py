"""
DEBUG de format_data_for_claude() - Dónde se pierden los datos
"""

import sys
sys.path.append('/home/claude')

from busqueda_flexible import get_facturacion_cliente, get_inversion_medios_cliente, get_ranking_dnit_cliente, convert_decimals_to_float
from sqlalchemy import create_engine
import os

# Configuración DB
DB_USER = 'postgres'
DB_PASS = '12345'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'jarvis'

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL, pool_pre_ping=True)

# Simular datos exactos que retorna get_facturacion_enriched()
def get_test_data():
    # Obtener datos reales de CERVEPAR
    facturacion = get_facturacion_cliente("cervepar", engine)
    inversion = get_inversion_medios_cliente("cervepar", engine, {'medio': 'TV'})
    ranking = get_ranking_dnit_cliente("cervepar", engine)
    
    # Construir estructura como lo hace get_facturacion_enriched()
    resultado = []
    if facturacion:
        for f in facturacion:
            resultado.append(f)
    
    if inversion and resultado:
        resultado[0]['inversion_medios'] = inversion
    
    if ranking and resultado:
        resultado[0]['ranking_dnit'] = ranking[0]
    
    return resultado

# COPIAR format_data_for_claude() actual del app.py para debug
def format_data_for_claude_debug(rows, query_type):
    """
    Copia con debug de la función format_data_for_claude()
    """
    print(f"🔧 format_data_for_claude() llamada:")
    print(f"   Rows: {len(rows) if rows else 0}")
    print(f"   Query type: '{query_type}'")
    
    if not rows:
        print("❌ Rows está vacío")
        return rows
    
    print(f"   Primer row tipo: {type(rows[0])}")
    print(f"   Primer row keys: {list(rows[0].keys()) if isinstance(rows[0], dict) else 'No es dict'}")
    
    # Si es query de facturación, SIEMPRE formatear para Claude
    if query_type == "facturacion" and isinstance(rows[0], dict):
        print("✅ Cumple condiciones para formatear")
        
        formatted = []
        for i, row in enumerate(rows):
            print(f"\n   📋 Procesando row {i+1}:")
            
            item = {
                'cliente': row.get('cliente', ''),
                'facturacion': row.get('facturacion_total', 0),
                'promedio_mensual': row.get('promedio_mensual', 0),
                'market_share': row.get('market_share', 0)
            }
            print(f"      Base item: {item}")
            
            # Agregar inversión si existe
            if 'inversion_medios' in row:
                print("      ✅ Procesando inversión...")
                inv = row['inversion_medios']
                print(f"         Inversión raw: {len(inv)} registros")
                item['inversion_detalle'] = inv
                item['inversion_total_usd'] = sum(i.get('inversion_usd', 0) for i in inv)
                print(f"         Total USD agregado: ${item['inversion_total_usd']:,.2f}")
            else:
                print("      ❌ NO hay inversión en row")
                item['inversion_detalle'] = []
                item['inversion_total_usd'] = 0
            
            # Agregar ranking si existe
            if 'ranking_dnit' in row:
                print("      ✅ Procesando ranking...")
                item['ranking'] = row['ranking_dnit'].get('ranking')
                item['aporte_dnit'] = row['ranking_dnit'].get('aporte_gs')
                print(f"         Ranking agregado: #{item['ranking']}")
            else:
                print("      ❌ NO hay ranking en row")
                item['ranking'] = None
                item['aporte_dnit'] = 0
            
            print(f"      Item final: {list(item.keys())}")
            formatted.append(item)
        
        print(f"\n✅ Formateado completado: {len(formatted)} items")
        return formatted
    else:
        print("❌ NO cumple condiciones para formatear")
        print(f"   query_type == 'facturacion': {query_type == 'facturacion'}")
        print(f"   isinstance(rows[0], dict): {isinstance(rows[0], dict)}")
    
    return rows

# ============================================================================
# TEST COMPLETO
# ============================================================================

try:
    print("🔧 DEBUG format_data_for_claude()")
    print("="*60)
    
    # 1. Obtener datos como los devuelve get_facturacion_enriched()
    print("1️⃣ Obteniendo datos de CERVEPAR...")
    test_data = get_test_data()
    
    if not test_data:
        print("❌ No se obtuvieron datos")
        exit()
    
    print(f"✅ Datos obtenidos:")
    print(f"   Estructura: {list(test_data[0].keys())}")
    print(f"   Tiene inversión: {'inversion_medios' in test_data[0]}")
    print(f"   Tiene ranking: {'ranking_dnit' in test_data[0]}")
    
    # 2. Procesar con format_data_for_claude()
    print(f"\n2️⃣ Procesando con format_data_for_claude()...")
    print("-" * 40)
    
    formatted = format_data_for_claude_debug(test_data, "facturacion")
    
    # 3. Verificar resultado
    print(f"\n3️⃣ RESULTADO FINAL:")
    print("-" * 40)
    
    if not formatted:
        print("❌ format_data_for_claude() retorna vacío")
    elif not isinstance(formatted[0], dict):
        print("❌ format_data_for_claude() no retorna dict")
    else:
        final_item = formatted[0]
        print(f"✅ Item final:")
        print(f"   Cliente: {final_item.get('cliente')}")
        print(f"   Facturación: {final_item.get('facturacion', 0):,.0f} Gs")
        print(f"   Inversión USD: ${final_item.get('inversion_total_usd', 0):,.2f}")
        print(f"   Ranking: #{final_item.get('ranking')}")
        
        # Verificar si Claude recibiría los datos completos
        if final_item.get('inversion_total_usd', 0) > 0:
            print("\n✅ CLAUDE RECIBIRÍA INVERSIÓN CORRECTAMENTE")
        else:
            print("\n❌ CLAUDE NO VERÍA LA INVERSIÓN")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

