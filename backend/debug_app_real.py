"""
DEBUG del app.py REAL - Encontrar por qué no funciona la inversión
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

# COPIA EXACTA de get_facturacion_enriched() del app.py
def get_facturacion_enriched_real(query):
    """
    COPIA EXACTA de la función del app.py para debug
    """
    query_limpio = query.replace('?', '').replace('!', '').replace(',', '').lower()
    print(f"🔍 Query limpio: '{query_limpio}'")
    
    # Palabras comunes a ignorar
    stopwords = ['cuanto', 'cuánto', 'facturo', 'facturó', 'facturacion', 'facturación', 
                 'de', 'la', 'el', 'en', 'y', 'o', 'para', 'con', 'a', 'un', 'una',
                 'invirtio', 'invirti', 'invertir', 'inversion']
    
    palabras = query_limpio.split()
    cliente_palabras = [p for p in palabras if p not in stopwords and len(p) > 2]
    print(f"🔍 Palabras filtradas: {cliente_palabras}")
    
    if not cliente_palabras:
        return []
    
    # Extraer nombre del cliente
    cliente = cliente_palabras[0] if len(cliente_palabras) == 1 else " ".join(cliente_palabras[:2])
    print(f"🔍 Cliente extraído: '{cliente}'")
    
    # Detectar qué datos necesita
    pide_inversion = any(w in query_limpio for w in ['tv', 'radio', 'cable', 'inversion', 'invirtio', 'invertir', 'medios', 'publicidad', 'pauta'])
    pide_ranking = any(w in query_limpio for w in ['ranking', 'dnit', 'posicion', 'puesto', 'aporte'])
    
    print(f"🔍 Detecta inversión: {pide_inversion} (busca: tv, radio, cable, inversion, invirtio, invertir, medios, publicidad, pauta)")
    print(f"🔍 Detecta ranking: {pide_ranking}")
    
    resultado = []
    
    try:
        # 1. Siempre buscar facturación si la query lo indica
        if any(w in query_limpio for w in ['facturo', 'facturacion', 'vendio', 'ventas', 'cuanto']):
            print("📊 Buscando facturación...")
            facturacion = get_facturacion_cliente(cliente, engine)
            print(f"📊 Facturación: {len(facturacion)} registros")
            
            if facturacion:
                # Agregar datos de facturación al resultado
                for f in facturacion:
                    resultado.append(f)
                print(f"📊 ✅ Cliente: {facturacion[0]['cliente']}, Facturación: {facturacion[0]['facturacion_total']:,.0f} Gs")
        
        # 2. Si pide inversión, buscar en medios
        if pide_inversion:
            print("📺 DEBERÍA buscar inversión...")
            # Detectar filtros
            filtros = {}
            if 'tv' in query_limpio:
                filtros['medio'] = 'TV'
                print(f"📺 Filtro TV detectado: {filtros}")
            elif 'radio' in query_limpio:
                filtros['medio'] = 'RADIO'
            elif 'cable' in query_limpio:
                filtros['medio'] = 'CABLE'
            
            print(f"📺 Llamando get_inversion_medios_cliente('{cliente}', engine, {filtros})")
            inversion = get_inversion_medios_cliente(cliente, engine, filtros)
            print(f"📺 Inversión retornada: {len(inversion)} registros")
            
            if inversion:
                print(f"📺 ✅ Inversión encontrada:")
                for i, inv in enumerate(inversion):
                    print(f"     {i+1}. {inv['medio']}: ${inv['inversion_usd']:,.2f}")
                
                # Agregar datos de inversión al resultado
                if resultado:
                    print("📺 ✅ Agregando inversión a facturación existente...")
                    resultado[0]['inversion_medios'] = inversion
                    print(f"📺 ✅ Resultado actualizado: {list(resultado[0].keys())}")
                else:
                    print("📺 ✅ Creando resultado solo con inversión...")
                    resultado = [{
                        'cliente': inversion[0]['cliente'],
                        'inversion_medios': inversion
                    }]
            else:
                print("📺 ❌ NO se encontró inversión")
        else:
            print("📺 ❌ NO detectó que pide inversión")
        
        # 3. Siempre buscar ranking DNIT cuando tenemos datos del cliente
        if resultado:
            print("🏆 Buscando ranking...")
            ranking = get_ranking_dnit_cliente(cliente, engine)
            print(f"🏆 Ranking: {len(ranking)} registros")
            
            if ranking:
                resultado[0]['ranking_dnit'] = ranking[0]
                print(f"🏆 ✅ Ranking: #{ranking[0]['ranking']}")
        
        print(f"\n📋 RESULTADO FINAL:")
        print(f"   Registros: {len(resultado)}")
        if resultado:
            print(f"   Estructura: {list(resultado[0].keys())}")
            print(f"   Tiene inversión: {'inversion_medios' in resultado[0]}")
            if 'inversion_medios' in resultado[0]:
                total_inv = sum(i.get('inversion_usd', 0) for i in resultado[0]['inversion_medios'])
                print(f"   Total inversión: ${total_inv:,.2f}")
        
        return resultado
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return []

# Test con la query exacta que falló
try:
    print("🚨 DEBUG APP.PY REAL")
    print("="*60)
    
    query = "cervepar cuanto facturo y cuanto invirtio en tv"
    print(f"Query: '{query}'")
    print("-" * 60)
    
    resultado = get_facturacion_enriched_real(query)
    
    if not resultado:
        print("\n❌ PROBLEMA: Sin resultado")
    elif 'inversion_medios' not in resultado[0]:
        print("\n❌ PROBLEMA: Facturación encontrada pero SIN inversión")
        print("    Este es el bug que está viendo Claude")
    else:
        print("\n✅ TODO OK: Facturación + Inversión encontrados")
        print("    Si esto funciona pero Claude no lo ve, el problema está en format_data_for_claude()")
    
except Exception as e:
    print(f"❌ ERROR CRÍTICO: {e}")
    import traceback
    traceback.print_exc()

