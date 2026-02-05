"""
TEST COMPLETO DEL FLUJO SIN CLAUDE API
Simula exactamente lo que hace /api/query hasta el punto de enviar datos a Claude
"""

import sys
import os
sys.path.append('.')  # Asume que ejecutas desde la carpeta del backend

# Importar las funciones del app.py actual
try:
    from busqueda_flexible import get_facturacion_cliente, get_inversion_medios_cliente, get_ranking_dnit_cliente
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    print("✅ Imports correctos")
except ImportError as e:
    print(f"❌ Error de import: {e}")
    print("Asegúrate de ejecutar desde la carpeta del backend")
    exit()

load_dotenv()

# Configuración DB
DB_USER = os.getenv('PG_USER', 'postgres')
DB_PASS = os.getenv('PG_PASS', '12345')
DB_HOST = os.getenv('PG_HOST', 'localhost')
DB_PORT = os.getenv('PG_PORT', '5432')
DB_NAME = os.getenv('PG_DB', 'jarvis')

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DB_URL, pool_pre_ping=True)
    print("✅ Conexión a BD establecida")
except Exception as e:
    print(f"❌ Error de conexión BD: {e}")
    exit()

# ============================================================================
# COPIAR FUNCIONES EXACTAS DEL APP.PY CORREGIDO
# ============================================================================

def format_data_for_claude_test(rows, query_type):
    """
    Copia exacta de format_data_for_claude() con debug
    """
    print(f"\n🔧 format_data_for_claude() TEST")
    print(f"   Input: {len(rows)} rows, query_type='{query_type}'")
    
    if not rows:
        print("❌ Rows vacío")
        return rows
    
    print(f"   Row[0] keys: {list(rows[0].keys())}")
    
    # ✅ CORREGIDO: Formatear SIEMPRE para queries de facturación
    if query_type == "facturacion" and isinstance(rows[0], dict):
        print("✅ Condición cumplida - formateando...")
        
        # Datos cruzados, formatear para Claude
        formatted = []
        for i, row in enumerate(rows):
            print(f"\n   📋 Procesando row {i+1}:")
            
            item = {
                'cliente': row.get('cliente', ''),
                'facturacion': row.get('facturacion_total', 0),  # ✅ Clave corregida
                'promedio_mensual': row.get('promedio_mensual', 0),
                'market_share': row.get('market_share', 0)
            }
            print(f"      Base: {item['cliente']}, Facturación: {item['facturacion']:,.0f}")
            
            # Agregar inversión si existe
            if 'inversion_medios' in row:
                inv = row['inversion_medios']
                item['inversion_detalle'] = inv
                item['inversion_total_usd'] = sum(i.get('inversion_usd', 0) for i in inv)
                print(f"      ✅ Inversión agregada: ${item['inversion_total_usd']:,.2f}")
            else:
                # ✅ Valores por defecto cuando no hay inversión
                item['inversion_detalle'] = []
                item['inversion_total_usd'] = 0
                print(f"      ❌ Sin inversión - valores por defecto")
            
            # Agregar ranking si existe
            if 'ranking_dnit' in row:
                item['ranking'] = row['ranking_dnit'].get('ranking')
                item['aporte_dnit'] = row['ranking_dnit'].get('aporte_gs')
                print(f"      ✅ Ranking agregado: #{item['ranking']}")
            else:
                # ✅ Valores por defecto cuando no hay ranking
                item['ranking'] = None
                item['aporte_dnit'] = 0
                print(f"      ❌ Sin ranking - valores por defecto")
            
            formatted.append(item)
        
        print(f"\n✅ Formateo completado: {len(formatted)} items")
        return formatted
    else:
        print("❌ No cumple condiciones para formatear")
    
    return rows

def get_facturacion_enriched_test(query):
    """
    Copia exacta de get_facturacion_enriched() con debug
    """
    print(f"\n🎯 get_facturacion_enriched() TEST")
    print(f"   Query: '{query}'")
    
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '').lower()
    print(f"   Query limpio: '{query_limpio}'")
    
    # Palabras comunes a ignorar
    stopwords = ['cuanto', 'cuánto', 'facturo', 'facturó', 'facturacion', 'facturación', 
                 'de', 'la', 'el', 'en', 'y', 'o', 'para', 'con', 'a', 'un', 'una',
                 'invirtio', 'invirti', 'invertir', 'inversion']
    
    palabras = query_limpio.split()
    cliente_palabras = [p for p in palabras if p not in stopwords and len(p) > 2]
    print(f"   Palabras filtradas: {cliente_palabras}")
    
    if not cliente_palabras:
        return []
    
    # Extraer nombre del cliente
    cliente = cliente_palabras[0] if len(cliente_palabras) == 1 else " ".join(cliente_palabras[:2])
    print(f"   Cliente extraído: '{cliente}'")
    
    # Detectar qué datos necesita
    pide_inversion = any(w in query_limpio for w in ['tv', 'radio', 'cable', 'inversion', 'invirtio', 'invertir', 'medios', 'publicidad', 'pauta'])
    pide_ranking = any(w in query_limpio for w in ['ranking', 'dnit', 'posicion', 'puesto', 'aporte'])
    
    print(f"   Detecta inversión: {pide_inversion}")
    print(f"   Detecta ranking: {pide_ranking}")
    
    resultado = []
    
    try:
        # 1. Siempre buscar facturación si la query lo indica
        if any(w in query_limpio for w in ['facturo', 'facturacion', 'vendio', 'ventas', 'cuanto']):
            print("   📊 Buscando facturación...")
            facturacion = get_facturacion_cliente(cliente, engine)
            print(f"   📊 Resultado: {len(facturacion)} registros")
            
            if facturacion:
                # Agregar datos de facturación al resultado
                for f in facturacion:
                    resultado.append(f)
                print(f"   📊 ✅ Cliente: {facturacion[0]['cliente']}")
        
        # 2. Si pide inversión, buscar en medios
        if pide_inversion:
            print("   📺 Buscando inversión...")
            # Detectar filtros
            filtros = {}
            if 'tv' in query_limpio:
                filtros['medio'] = 'TV'
                print(f"   📺 Filtro TV aplicado: {filtros}")
            elif 'radio' in query_limpio:
                filtros['medio'] = 'RADIO'
            elif 'cable' in query_limpio:
                filtros['medio'] = 'CABLE'
            
            inversion = get_inversion_medios_cliente(cliente, engine, filtros)
            print(f"   📺 Resultado: {len(inversion)} registros")
            
            if inversion:
                # Agregar datos de inversión al resultado
                if resultado:
                    # Ya hay facturación, agregar inversión al mismo dict
                    resultado[0]['inversion_medios'] = inversion
                    print("   📺 ✅ Inversión agregada a facturación")
                else:
                    # Solo inversión, crear resultado
                    resultado = [{
                        'cliente': inversion[0]['cliente'],
                        'inversion_medios': inversion
                    }]
                    print("   📺 ✅ Resultado creado con solo inversión")
            else:
                print("   📺 ❌ Sin inversión encontrada")
        
        # 3. ✅ CORREGIDO: Siempre buscar ranking DNIT cuando tenemos datos del cliente
        if resultado:  # ✅ CAMBIO: buscar automáticamente
            print("   🏆 Buscando ranking (automáticamente)...")
            ranking = get_ranking_dnit_cliente(cliente, engine)
            print(f"   🏆 Resultado: {len(ranking)} registros")
            
            if ranking:
                resultado[0]['ranking_dnit'] = ranking[0]
                print(f"   🏆 ✅ Ranking agregado: #{ranking[0]['ranking']}")
            else:
                print("   🏆 ❌ Sin ranking encontrado")
        
        print(f"\n   📋 RESULTADO FINAL: {len(resultado)} registros")
        if resultado:
            print(f"   📋 Estructura: {list(resultado[0].keys())}")
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

# ============================================================================
# TEST COMPLETO
# ============================================================================

def test_query_completo(user_query):
    """
    Simula el endpoint /api/query completo hasta el punto de enviar a Claude
    """
    print("="*80)
    print(f"🧪 TEST COMPLETO: '{user_query}'")
    print("="*80)
    
    query_lower = user_query.lower()
    
    # DETECCIÓN DE TIPO DE QUERY (igual que en app.py)
    rows = []
    query_type = "generico"
    
    if any(w in query_lower for w in ["top", "ranking", "principal", "importante", "mayor", "más", "clientes"]):
        query_type = "ranking"
        print("🔍 Detectado: ranking")
        # No probamos ranking por ahora, solo facturación
        return
        
    elif any(w in query_lower for w in ["cuánto", "cuanto", "factur", "how much", "invirti", "ranking", "dnit"]):
        query_type = "facturacion"
        print("🔍 Detectado: facturacion")
        
        # Llamar get_facturacion_enriched()
        rows = get_facturacion_enriched_test(user_query)
        
        if not rows:
            print("❌ get_facturacion_enriched() retornó vacío")
            return
        
        # Llamar format_data_for_claude()
        formatted_rows = format_data_for_claude_test(rows, query_type)
        
        if not formatted_rows:
            print("❌ format_data_for_claude() retornó vacío")
            return
        
        # MOSTRAR QUÉ RECIBIRÍA CLAUDE
        print("\n" + "="*80)
        print("🎯 DATOS QUE RECIBIRÍA CLAUDE API:")
        print("="*80)
        
        final_data = formatted_rows[0]
        print(f"Cliente: {final_data.get('cliente')}")
        print(f"Facturación: {final_data.get('facturacion', 0):,.0f} Gs")
        print(f"Market Share: {final_data.get('market_share', 0)}%")
        print(f"Inversión USD: ${final_data.get('inversion_total_usd', 0):,.2f}")
        print(f"Ranking DNIT: #{final_data.get('ranking') or 'Sin datos'}")
        print(f"Aporte DNIT: {final_data.get('aporte_dnit', 0):,.0f} Gs")
        
        if final_data.get('inversion_detalle'):
            print(f"\n📺 DETALLE INVERSIÓN:")
            for inv in final_data['inversion_detalle']:
                print(f"   {inv['medio']}: ${inv['inversion_usd']:,.2f}")
        
        # PREDICCIÓN DE RESPUESTA
        print("\n" + "="*80)
        print("💬 PREDICCIÓN DE RESPUESTA DE CLAUDE:")
        print("="*80)
        
        if final_data.get('inversion_total_usd', 0) > 0 and final_data.get('ranking'):
            print("✅ RESPUESTA COMPLETA ESPERADA:")
            print(f"   '{final_data.get('cliente')}' facturó {final_data.get('facturacion', 0):,.0f} Gs")
            print(f"   e invirtió ${final_data.get('inversion_total_usd', 0):,.2f} USD en televisión.")
            print(f"   Con ranking DNIT #{final_data.get('ranking')}, es un cliente estratégico...")
            
        elif final_data.get('inversion_total_usd', 0) > 0:
            print("✅ RESPUESTA CON INVERSIÓN (sin ranking):")
            print(f"   '{final_data.get('cliente')}' facturó {final_data.get('facturacion', 0):,.0f} Gs")
            print(f"   e invirtió ${final_data.get('inversion_total_usd', 0):,.2f} USD en televisión.")
            
        elif final_data.get('ranking'):
            print("✅ RESPUESTA CON RANKING (sin inversión):")
            print(f"   '{final_data.get('cliente')}' facturó {final_data.get('facturacion', 0):,.0f} Gs")
            print(f"   pero no registra inversión en televisión. Ranking DNIT #{final_data.get('ranking')}...")
            
        else:
            print("⚠️ RESPUESTA SOLO FACTURACIÓN:")
            print(f"   '{final_data.get('cliente')}' facturó {final_data.get('facturacion', 0):,.0f} Gs")
            print(f"   pero no registra inversión en televisión ni ranking DNIT.")
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETADO SIN USAR CLAUDE API")
    print("="*80)

# ============================================================================
# CASOS DE PRUEBA
# ============================================================================

if __name__ == "__main__":
    # Test cases
    test_cases = [
        "cervepar cuanto facturo y cuanto invirtio en tv",
        "telefonica cuanto facturo y cuanto invirtio en tv", 
        "unilever cuanto facturo y cuanto invirtio en tv"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n🧪 CASO {i}/{len(test_cases)}")
        test_query_completo(query)
        
        if i < len(test_cases):
            input("\n⏸️ Presiona Enter para el siguiente caso...")

