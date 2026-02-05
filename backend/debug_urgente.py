"""
DEBUG URGENTE: ¿Qué versión de las funciones se está ejecutando?
"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine
from dotenv import load_dotenv
from busqueda_flexible import get_facturacion_cliente, get_inversion_medios_cliente, get_ranking_dnit_cliente

load_dotenv()

# Configuración DB
DB_USER = os.getenv('PG_USER', 'postgres')
DB_PASS = os.getenv('PG_PASS', '12345')
DB_HOST = os.getenv('PG_HOST', 'localhost')
DB_PORT = os.getenv('PG_PORT', '5432')
DB_NAME = os.getenv('PG_DB', 'jarvis')

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL, pool_pre_ping=True)

def debug_app_actual():
    """
    Debug del app.py que está ejecutándose AHORA
    """
    print("🚨 DEBUG URGENTE - VERIFICAR APP.PY ACTUAL")
    print("="*60)
    
    try:
        # Importar desde el app.py actual
        import app
        print("✅ app.py importado")
        
        # Verificar si tiene las funciones corregidas
        if hasattr(app, 'get_facturacion_enriched'):
            print("✅ get_facturacion_enriched() existe")
        else:
            print("❌ get_facturacion_enriched() NO EXISTE")
            
        if hasattr(app, 'format_data_for_claude'):
            print("✅ format_data_for_claude() existe")
        else:
            print("❌ format_data_for_claude() NO EXISTE")
            
        # Test directo con query de CERVEPAR
        print(f"\n🔍 TEST DIRECTO CON APP.PY ACTUAL:")
        print("-" * 40)
        
        query = "cervepar cuanto facturo y cuanto invirtio en tv"
        print(f"Query: {query}")
        
        # Llamar get_facturacion_enriched del app.py actual
        if hasattr(app, 'get_facturacion_enriched'):
            rows = app.get_facturacion_enriched(query)
            print(f"get_facturacion_enriched() retorna: {len(rows)} registros")
            
            if rows:
                print(f"Estructura: {list(rows[0].keys())}")
                print(f"Tiene inversión: {'inversion_medios' in rows[0]}")
                print(f"Tiene ranking: {'ranking_dnit' in rows[0]}")
                
                if 'inversion_medios' in rows[0]:
                    total_inv = sum(i.get('inversion_usd', 0) for i in rows[0]['inversion_medios'])
                    print(f"Total inversión: ${total_inv:,.2f}")
                
                # Llamar format_data_for_claude del app.py actual  
                if hasattr(app, 'format_data_for_claude'):
                    formatted = app.format_data_for_claude(rows, "facturacion")
                    print(f"format_data_for_claude() retorna: {len(formatted)} registros")
                    
                    if formatted and isinstance(formatted[0], dict):
                        final_data = formatted[0]
                        print(f"\n📋 DATOS FINALES:")
                        print(f"   Cliente: {final_data.get('cliente')}")
                        print(f"   Facturación: {final_data.get('facturacion', 0):,.0f}")
                        print(f"   Inversión: ${final_data.get('inversion_total_usd', 0):,.2f}")
                        print(f"   Ranking: #{final_data.get('ranking')}")
                        
                        if final_data.get('inversion_total_usd', 0) > 0:
                            print("✅ CLAUDE DEBERÍA VER LA INVERSIÓN")
                        else:
                            print("❌ CLAUDE NO VA A VER LA INVERSIÓN")
                            print("🚨 PROBLEMA: format_data_for_claude() no está funcionando")
                    else:
                        print("❌ format_data_for_claude() no retorna dict válido")
                else:
                    print("❌ format_data_for_claude() NO EXISTE en app.py")
            else:
                print("❌ get_facturacion_enriched() retorna vacío")
        else:
            print("❌ get_facturacion_enriched() NO EXISTE en app.py")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def verificar_archivos():
    """
    Verificar qué archivos hay y cuándo se modificaron
    """
    print(f"\n📁 VERIFICAR ARCHIVOS:")
    print("-" * 40)
    
    files_to_check = ['app.py', 'app_completo_corregido.py', 'app_backup.py']
    
    for filename in files_to_check:
        if os.path.exists(filename):
            stat = os.stat(filename)
            size = stat.st_size
            mtime = stat.st_mtime
            from datetime import datetime
            mod_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"✅ {filename}: {size:,} bytes, modificado: {mod_time}")
        else:
            print(f"❌ {filename}: NO EXISTE")

if __name__ == "__main__":
    verificar_archivos()
    debug_app_actual()

