"""
TEST DE DATOS PARCIALES - Casos específicos identificados
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
            
            inversion = get_inversion_medios_cliente(cliente, engine, filtros)
            if inversion:
                if resultado:
                    resultado[0]['inversion_medios'] = inversion
                else:
                    resultado = [{'cliente': inversion[0]['cliente'], 'inversion_medios': inversion}]
        
        # 3. Siempre buscar ranking DNIT cuando tenemos datos del cliente
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
        if query_type == "facturacion" and isinstance(rows[0], dict):
    # ✅ Formatear SIEMPRE + agregar valores por defecto
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
                else:
                    # ✅ AGREGAR campos vacíos cuando no hay inversión
                    item['inversion_detalle'] = []
                    item['inversion_total_usd'] = 0
                
                if 'ranking_dnit' in row:
                    item['ranking'] = row['ranking_dnit'].get('ranking')
                    item['aporte_dnit'] = row['ranking_dnit'].get('aporte_gs')
                else:
                    # ✅ AGREGAR campos vacíos cuando no hay ranking
                    item['ranking'] = None
                    item['aporte_dnit'] = 0
                
                formatted.append(item)
            return formatted
    
    return rows

# ============================================================================
# CASOS DE PRUEBA
# ============================================================================

test_cases = [
    {
        'nombre': 'TELEFONICA - Solo facturación (sin inversión, sin ranking)',
        'query': 'telefonica cuanto facturo y cuanto invirtio en tv',
        'esperado': {
            'facturacion': 'SÍ',
            'inversion': 'NO',
            'ranking': 'NO'
        }
    },
    {
        'nombre': 'UNILEVER - Con facturación, sin inversión, posible ranking', 
        'query': 'unilever cuanto facturo y cuanto invirtio en tv',
        'esperado': {
            'facturacion': 'SÍ',
            'inversion': 'NO', 
            'ranking': '?'
        }
    },
    {
        'nombre': 'CERVECERIA PARAGUAYA - Solo ranking (no es cliente)',
        'query': 'cerveceria paraguaya cuanto facturo',
        'esperado': {
            'facturacion': 'NO',
            'inversion': 'NO',
            'ranking': 'SÍ (pero busca por nombre directo)'
        }
    }
]

try:
    print("🧪 TEST DE DATOS PARCIALES")
    print("="*70)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ {test['nombre']}")
        print("-" * 60)
        print(f"Query: {test['query']}")
        
        # Ejecutar test
        rows = get_facturacion_enriched_v2(test['query'])
        
        if not rows:
            print("❌ Sin resultados")
            continue
            
        print(f"✅ Retorna: {len(rows)} registros")
        print(f"   Estructura: {list(rows[0].keys())}")
        
        # Analizar qué datos tiene
        has_facturacion = 'facturacion_total' in rows[0] and rows[0]['facturacion_total'] > 0
        has_inversion = 'inversion_medios' in rows[0]
        has_ranking = 'ranking_dnit' in rows[0]
        
        print(f"   📊 Facturación: {'✅ SÍ' if has_facturacion else '❌ NO'}")
        print(f"   📺 Inversión: {'✅ SÍ' if has_inversion else '❌ NO'}")
        print(f"   🏆 Ranking: {'✅ SÍ' if has_ranking else '❌ NO'}")
        
        # Formatear para Claude
        formatted = format_data_for_claude(rows, "facturacion")
        
        if formatted:
            final_data = formatted[0]
            print("\n   📋 DATOS PARA CLAUDE:")
            print(f"      Cliente: {final_data.get('cliente')}")
            print(f"      Facturación: {final_data.get('facturacion'):,.0f} Gs")
            print(f"      Inversión USD: ${final_data.get('inversion_total_usd', 0):,.2f}")
            print(f"      Ranking DNIT: {final_data.get('ranking') or 'Sin datos'}")
            print(f"      Aporte DNIT: {final_data.get('aporte_dnit', 0):,.0f} Gs")
        
        print(f"\n   🎯 Esperado: {test['esperado']}")
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS DE DATOS PARCIALES COMPLETADO")
    print("📝 Esto muestra cómo Claude va a manejar casos con información incompleta")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

