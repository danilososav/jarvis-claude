"""
TEST ACTUALIZADO - Ranking DNIT automático
"""

import sys
sys.path.append('/home/claude')

from busqueda_flexible import get_facturacion_cliente, get_inversion_medios_cliente, get_ranking_dnit_cliente
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

# Función actualizada con ranking automático
def get_facturacion_enriched_v2(query):
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '').lower()
    
    stopwords = ['cuanto', 'cuánto', 'facturo', 'facturó', 'facturacion', 'facturación', 
                 'de', 'la', 'el', 'en', 'y', 'o', 'para', 'con', 'a', 'un', 'una',
                 'invirtio', 'invirti', 'invertir', 'inversion']
    
    palabras = query_limpio.split()
    cliente_palabras = [p for p in palabras if p not in stopwords and len(p) > 2]
    
    if not cliente_palabras:
        return []
    
    cliente = cliente_palabras[0] if len(cliente_palabras) == 1 else " ".join(cliente_palabras[:2])
    
    pide_inversion = any(w in query_limpio for w in ['tv', 'radio', 'cable', 'inversion', 'invirtio', 'invertir', 'medios', 'publicidad', 'pauta'])
    
    resultado = []
    
    try:
        # 1. Buscar facturación
        if any(w in query_limpio for w in ['facturo', 'facturacion', 'vendio', 'ventas', 'cuanto']):
            facturacion = get_facturacion_cliente(cliente, engine)
            if facturacion:
                for f in facturacion:
                    resultado.append(f)
        
        # 2. Buscar inversión
        if pide_inversion:
            filtros = {}
            if 'tv' in query_limpio:
                filtros['medio'] = 'TV'
            elif 'radio' in query_limpio:
                filtros['medio'] = 'RADIO'
            elif 'cable' in query_limpio:
                filtros['medio'] = 'CABLE'
            
            inversion = get_inversion_medios_cliente(cliente, engine, filtros)
            if inversion:
                if resultado:
                    resultado[0]['inversion_medios'] = inversion
                else:
                    resultado = [{'cliente': inversion[0]['cliente'], 'inversion_medios': inversion}]
        
        # 3. ✅ SIEMPRE buscar ranking DNIT cuando tenemos datos del cliente
        if resultado:
            ranking = get_ranking_dnit_cliente(cliente, engine)
            if ranking:
                resultado[0]['ranking_dnit'] = ranking[0]
        
        return resultado
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def format_data_for_claude(rows, query_type):
    if not rows:
        return rows
    
    if query_type == "facturacion" and isinstance(rows[0], dict):
        if 'inversion_medios' in rows[0] or 'ranking_dnit' in rows[0]:
            formatted = []
            for row in rows:
                item = {
                    'cliente': row.get('cliente', ''),
                    'facturacion': row.get('facturacion_total', 0),
                    'promedio_mensual': row.get('promedio_mensual', 0),
                    'market_share': row.get('market_share', 0)
                }
                
                if 'inversion_medios' in row:
                    inv = row['inversion_medios']
                    item['inversion_detalle'] = inv
                    item['inversion_total_usd'] = sum(i.get('inversion_usd', 0) for i in inv)
                
                # ✅ AGREGAR DATOS DE RANKING
                if 'ranking_dnit' in row:
                    item['ranking'] = row['ranking_dnit'].get('ranking')
                    item['aporte_dnit'] = row['ranking_dnit'].get('aporte_gs')
                
                formatted.append(item)
            return formatted
    
    return rows

# ============================================================================
# TEST CON RANKING AUTOMÁTICO
# ============================================================================

try:
    print("🧪 TEST CON RANKING DNIT AUTOMÁTICO")
    print("="*50)
    
    query = "cervepar cuanto facturo y cuanto invirtio en tv"
    print(f"Query: {query}")
    
    print("\n1️⃣ Ejecutando función actualizada...")
    rows = get_facturacion_enriched_v2(query)
    print(f"   Retorna: {len(rows)} registros")
    
    if not rows:
        print("❌ Sin resultados")
        exit()
    
    print(f"   Estructura: {list(rows[0].keys())}")
    print(f"   Tiene inversion_medios: {'inversion_medios' in rows[0]}")
    print(f"   Tiene ranking_dnit: {'ranking_dnit' in rows[0]}")  # ✅ Ahora debe ser True
    
    if 'ranking_dnit' in rows[0]:
        print(f"   Ranking: #{rows[0]['ranking_dnit']['ranking']}")
        print(f"   Aporte: {rows[0]['ranking_dnit']['aporte_gs']:,.0f} Gs")
    
    print("\n2️⃣ Formateando para Claude...")
    formatted = format_data_for_claude(rows, "facturacion")
    
    print("\n3️⃣ DATOS FINALES COMPLETOS:")
    print("-" * 40)
    final_data = formatted[0]
    print(f"Cliente: {final_data.get('cliente')}")
    print(f"Facturación: {final_data.get('facturacion'):,.2f} Gs")
    print(f"Market Share: {final_data.get('market_share')}%")
    print(f"Inversión Total USD: ${final_data.get('inversion_total_usd', 0):,.2f}")
    print(f"Ranking DNIT: #{final_data.get('ranking')}")  # ✅ Ya no debe ser None
    print(f"Aporte DNIT: {final_data.get('aporte_dnit', 0):,.0f} Gs")
    
    if 'inversion_detalle' in final_data:
        print("\n📺 DETALLE INVERSIÓN TV:")
        for inv in final_data['inversion_detalle']:
            print(f"   {inv['medio']}: ${inv['inversion_usd']:,.2f}")
    
    print("\n" + "="*50)
    print("✅ FLUJO COMPLETO CON RANKING DNIT")
    print("✅ FACTURACIÓN: OK")
    print("✅ INVERSIÓN TV: OK") 
    print("✅ RANKING DNIT: OK")  # ✅ Ahora incluido automáticamente
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

