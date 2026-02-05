"""
DEBUG COMPLETO - Sin Claude API
Verificar paso a paso qué está fallando
"""

import sys
sys.path.append('/home/claude')

from busqueda_flexible import (
    buscar_anunciante, 
    get_facturacion_cliente, 
    get_inversion_medios_cliente,
    get_ranking_dnit_cliente
)
from sqlalchemy import create_engine, text
import os

# Configuración DB (ajustar según tu .env)
DB_USER = 'postgres'
DB_PASS = '12345'  # Cambiar por tu password
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'jarvis'

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DB_URL, pool_pre_ping=True)
    print("✅ Conectado a PostgreSQL")
    
    print("\n" + "="*60)
    print("PASO 1: Verificar que CERVEPAR existe")
    print("="*60)
    
    # Test buscar_anunciante
    anunciante = buscar_anunciante("cervepar", engine)
    print(f"Resultado: {anunciante}")
    
    if not anunciante:
        print("❌ CERVEPAR no encontrado - PROBLEMA CRÍTICO")
        exit()
    
    print(f"✅ CERVEPAR encontrado - ID: {anunciante['anunciante_id']}")
    
    print("\n" + "="*60)
    print("PASO 2: Verificar facturación directa en BD")
    print("="*60)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as registros,
                ROUND(SUM(facturacion), 2) as total_facturacion
            FROM fact_facturacion 
            WHERE anunciante_id = :aid
        """), {'aid': anunciante['anunciante_id']}).fetchone()
        
        print(f"BD Directa - Registros: {result[0]}, Total: {result[1]:,.2f} Gs")
    
    print("\n" + "="*60)
    print("PASO 3: Test get_facturacion_cliente()")
    print("="*60)
    
    facturacion = get_facturacion_cliente("cervepar", engine)
    print(f"Función retorna: {len(facturacion)} registros")
    if facturacion:
        print(f"Datos: {facturacion[0]}")
    else:
        print("❌ Función retorna vacío")
    
    print("\n" + "="*60)
    print("PASO 4: Verificar inversión directa en BD")
    print("="*60)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                medio,
                COUNT(*) as registros,
                ROUND(SUM(monto_usd), 2) as total_usd
            FROM fact_inversion_medios 
            WHERE anunciante_id = :aid
              AND UPPER(medio) LIKE '%TV%'
            GROUP BY medio
            ORDER BY total_usd DESC
        """), {'aid': anunciante['anunciante_id']}).fetchall()
        
        print("BD Directa - Inversión TV:")
        total = 0
        for row in result:
            print(f"  {row[0]}: {row[1]} registros, ${row[2]:,.2f}")
            total += row[2]
        print(f"  TOTAL TV: ${total:,.2f}")
    
    print("\n" + "="*60)
    print("PASO 5: Test get_inversion_medios_cliente()")
    print("="*60)
    
    inversion = get_inversion_medios_cliente("cervepar", engine, {'medio': 'TV'})
    print(f"Función retorna: {len(inversion)} registros")
    if inversion:
        for i, row in enumerate(inversion):
            print(f"  {i+1}. {row}")
    else:
        print("❌ Función retorna vacío")
    
    print("\n" + "="*60)
    print("PASO 6: Test get_ranking_dnit_cliente()")
    print("="*60)
    
    ranking = get_ranking_dnit_cliente("cervepar", engine)
    print(f"Función retorna: {len(ranking)} registros")
    if ranking:
        print(f"Datos: {ranking[0]}")
    else:
        print("❌ Función retorna vacío")
        
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    print(f"✅ CERVEPAR ID: {anunciante['anunciante_id']}")
    print(f"📊 Facturación: {'✅ OK' if facturacion else '❌ FALLA'}")
    print(f"📺 Inversión TV: {'✅ OK' if inversion else '❌ FALLA'}")
    print(f"🏆 Ranking DNIT: {'✅ OK' if ranking else '❌ FALLA'}")
    
except Exception as e:
    print(f"❌ ERROR CRÍTICO: {e}")
    import traceback
    traceback.print_exc()

