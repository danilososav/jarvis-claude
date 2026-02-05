"""
DEBUG ESPECÍFICO DEL ENDPOINT /api/query
Verificar si el endpoint está usando las funciones corregidas
"""

import sys
import os
sys.path.append('.')

def debug_endpoint_query():
    """
    Verificar qué está haciendo el endpoint /api/query exactamente
    """
    print("🔍 DEBUG ENDPOINT /api/query")
    print("="*50)
    
    try:
        import app
        
        # Buscar el endpoint query en app.py
        import inspect
        
        # Obtener el código fuente de la función query
        if hasattr(app, 'query'):
            print("✅ Endpoint query() encontrado")
            
            # Obtener código fuente
            source = inspect.getsource(app.query)
            
            # Buscar llamadas específicas
            print(f"\n🔍 VERIFICAR LLAMADAS EN ENDPOINT:")
            print("-" * 40)
            
            # 1. ¿Llama a get_facturacion_enriched?
            if 'get_facturacion_enriched' in source:
                print("✅ SÍ llama a get_facturacion_enriched()")
            else:
                print("❌ NO llama a get_facturacion_enriched()")
            
            # 2. ¿Llama a format_data_for_claude?  
            if 'format_data_for_claude' in source:
                print("✅ SÍ llama a format_data_for_claude()")
                
                # Ver el contexto de la llamada
                lines = source.split('\n')
                for i, line in enumerate(lines):
                    if 'format_data_for_claude' in line:
                        print(f"   Línea {i}: {line.strip()}")
                        if i > 0:
                            print(f"   Línea {i-1}: {lines[i-1].strip()}")
                        if i < len(lines) - 1:
                            print(f"   Línea {i+1}: {lines[i+1].strip()}")
            else:
                print("❌ NO llama a format_data_for_claude()")
                print("🚨 PROBLEMA: El endpoint no está formateando los datos")
                
            # 3. ¿Llama a generate_response?
            if 'generate_response' in source:
                print("✅ SÍ llama a generate_response()")
            else:
                print("❌ NO llama a generate_response()")
                
            # Mostrar las líneas relevantes del endpoint
            print(f"\n📋 CÓDIGO RELEVANTE DEL ENDPOINT:")
            print("-" * 40)
            
            lines = source.split('\n')
            in_facturacion_section = False
            
            for i, line in enumerate(lines):
                # Buscar la sección de facturación
                if 'facturacion' in line.lower() and ('query_type' in line or 'detectado' in line):
                    in_facturacion_section = True
                    print(f"{i+1:3d}: {line}")
                elif in_facturacion_section:
                    print(f"{i+1:3d}: {line}")
                    # Dejar de mostrar después de unas líneas
                    if line.strip() == '' and i > 0 and lines[i-1].strip() == '':
                        break
                    if 'return jsonify' in line:
                        break
        else:
            print("❌ Endpoint query() NO encontrado")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def buscar_llamadas_format_data():
    """
    Buscar todas las referencias a format_data_for_claude en el código
    """
    print(f"\n🔎 BUSCAR TODAS LAS LLAMADAS A format_data_for_claude:")
    print("-" * 50)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if 'format_data_for_claude' in line:
                print(f"Línea {i}: {line.strip()}")
                
    except Exception as e:
        print(f"❌ Error leyendo app.py: {e}")

if __name__ == "__main__":
    debug_endpoint_query()
    buscar_llamadas_format_data()

