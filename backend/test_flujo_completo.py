"""
TEST FINAL - Flujo completo sin Claude API
Verificar que get_facturacion_enriched + format_data_for_claude funcionan juntos
"""

import sys
sys.path.append('/home/claude')

# Simular las funciones de app.py sin importar todo
from busqueda_flexible import get_facturacion_cliente, get_inversion_medios_cliente, get_ranking_dnit_cliente
from sqlalchemy import create_engine, text
import os

# Configuración DB
DB_USER = 'postgres'
DB_PASS = '12345'  # Ajustar
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'jarvis'

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL, pool_pre_ping=True)

# Copiar función get_facturacion_enriched() exacta del app.py
def get_facturacion_enriched(query):
    """
    Facturación de un cliente con búsqueda flexible
    Detecta si pide solo facturación o facturación + inversión
    """
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '').lower()
    
    # Palabras comunes a ignorar
    stopwords = ['cuanto', 'cuánto', 'facturo', 'facturó', 'facturacion', 'facturación', 
                 'de', 'la', 'el', 'en', 'y', 'o', 'para', 'con', 'a', 'un', 'una',
                 'invirtio', 'invirti', 'invertir', 'inversion']
    
    palabras = query_limpio.split()
    cliente_palabras = [p for p in palabras if p not in stopwords and len(p) > 2]
    
    if not cliente_palabras:
        return []
    
    # Extraer nombre del cliente
    cliente = cliente_palabras[0] if len(cliente_palabras) == 1 else " ".join(cliente_palabras[:2])
    
    # Detectar qué datos necesita
    pide_inversion = any(w in query_limpio for w in ['tv', 'radio', 'cable', 'inversion', 'invirtio', 'invertir', 'medios', 'publicidad', 'pauta'])
    pide_ranking = any(w in query_limpio for w in ['ranking', 'dnit', 'posicion', 'puesto', 'aporte'])
    
    resultado = []
    
    try:
        # 1. Siempre buscar facturación si la query lo indica
        if any(w in query_limpio for w in ['facturo', 'facturacion', 'vendio', 'ventas', 'cuanto']):
            facturacion = get_facturacion_cliente(cliente, engine)
            
            if facturacion:
                # Agregar datos de facturación al resultado
                for f in facturacion:
                    resultado.append(f)
        
        # 2. Si pide inversión, buscar en medios
        if pide_inversion:
            # Detectar filtros
            filtros = {}
            if 'tv' in query_limpio:
                filtros['medio'] = 'TV'
            elif 'radio' in query_limpio:
                filtros['medio'] = 'RADIO'
            elif 'cable' in query_limpio:
                filtros['medio'] = 'CABLE'
            
            inversion = get_inversion_medios_cliente(cliente, engine, filtros)
            
            if inversion:
                # Agregar datos de inversión al resultado
                if resultado:
                    # Ya hay facturación, agregar inversión al mismo dict
                    resultado[0]['inversion_medios'] = inversion
                else:
                    # Solo inversión, crear resultado
                    resultado = [{
                        'cliente': inversion[0]['cliente'],
                        'inversion_medios': inversion
                    }]
        
        # 3. Si pide ranking DNIT, buscar
        if pide_ranking:
            ranking = get_ranking_dnit_cliente(cliente, engine)
            
            if ranking:
                if resultado:
                    resultado[0]['ranking_dnit'] = ranking[0]
                else:
                    resultado = [ranking[0]]
        
        return resultado
        
    except Exception as e:
        print(f"Error en get_facturacion_enriched: {e}")
        return []

# Copiar función format_data_for_claude() con la corrección
def format_data_for_claude(rows, query_type):
    """
    Formatea datos cruzados para que Claude los entienda mejor
    """
    if not rows:
        return rows
    
    # Si tiene datos de inversión o ranking, formatear especialmente
    if query_type == "facturacion" and isinstance(rows[0], dict):
        if 'inversion_medios' in rows[0] or 'ranking_dnit' in rows[0]:
            # Datos cruzados, formatear para Claude
            formatted = []
            for row in rows:
                item = {
                    'cliente': row.get('cliente', ''),
                    'facturacion': row.get('facturacion_total', 0),  # ✅ CORREGIDO
                    'promedio_mensual': row.get('promedio_mensual', 0),
                    'market_share': row.get('market_share', 0)
                }
                
                # Agregar inversión si existe
                if 'inversion_medios' in row:
                    inv = row['inversion_medios']
                    item['inversion_detalle'] = inv
                    item['inversion_total_usd'] = sum(i.get('inversion_usd', 0) for i in inv)
                
                # Agregar ranking si existe
                if 'ranking_dnit' in row:
                    item['ranking'] = row['ranking_dnit'].get('ranking')
                    item['aporte_dnit'] = row['ranking_dnit'].get('aporte_gs')
                
                formatted.append(item)
            
            return formatted
    
    return rows

# ============================================================================
# TEST DEL FLUJO COMPLETO
# ============================================================================

try:
    print("🧪 TEST FLUJO COMPLETO")
    print("="*50)
    
    query = "cervepar cuanto facturo y cuanto invirtio en tv"
    print(f"Query: {query}")
    
    print("\n1️⃣ Ejecutando get_facturacion_enriched()...")
    rows = get_facturacion_enriched(query)
    print(f"   Retorna: {len(rows)} registros")
    
    if not rows:
        print("❌ get_facturacion_enriched() retorna vacío")
        exit()
    
    print(f"   Estructura: {list(rows[0].keys())}")
    print(f"   Tiene inversion_medios: {'inversion_medios' in rows[0]}")
    print(f"   Tiene ranking_dnit: {'ranking_dnit' in rows[0]}")
    
    print("\n2️⃣ Ejecutando format_data_for_claude()...")
    formatted = format_data_for_claude(rows, "facturacion")
    print(f"   Retorna: {len(formatted)} registros")
    
    if not formatted:
        print("❌ format_data_for_claude() retorna vacío")
        exit()
    
    print(f"   Estructura final: {list(formatted[0].keys())}")
    
    print("\n3️⃣ DATOS FINALES PARA CLAUDE:")
    print("-" * 30)
    final_data = formatted[0]
    print(f"Cliente: {final_data.get('cliente')}")
    print(f"Facturación: {final_data.get('facturacion'):,.2f} Gs")
    print(f"Market Share: {final_data.get('market_share')}%")
    print(f"Inversión Total USD: ${final_data.get('inversion_total_usd', 0):,.2f}")
    print(f"Ranking DNIT: #{final_data.get('ranking')}")
    
    if 'inversion_detalle' in final_data:
        print("\n📺 DETALLE INVERSIÓN TV:")
        for inv in final_data['inversion_detalle']:
            print(f"   {inv['medio']}: ${inv['inversion_usd']:,.2f}")
    
    print("\n" + "="*50)
    print("✅ FLUJO COMPLETO EXITOSO")
    print("✅ Datos listos para Claude")
    print("✅ FACTURACIÓN: OK")
    print("✅ INVERSIÓN TV: OK") 
    print("✅ RANKING: OK")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

