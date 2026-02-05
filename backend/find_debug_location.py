"""
Encontrar exactamente dónde están las llamadas a generate_response
"""

import sys
import os

def find_generate_response_calls():
    """
    Buscar todas las llamadas a generate_response y mostrar contexto
    """
    print("🔍 BUSCANDO generate_response EN APP.PY")
    print("="*60)
    
    if not os.path.exists('app.py'):
        print("❌ app.py no encontrado")
        return
        
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"✅ app.py tiene {len(lines)} líneas")
        
        found_calls = []
        
        for i, line in enumerate(lines, 1):
            if 'generate_response' in line and not line.strip().startswith('def '):
                found_calls.append(i)
                
        print(f"✅ Encontradas {len(found_calls)} llamadas a generate_response")
        
        for call_line in found_calls:
            print(f"\n📍 LLAMADA EN LÍNEA {call_line}:")
            print("-" * 40)
            
            # Mostrar contexto: 5 líneas antes y 5 después
            start = max(0, call_line - 6)
            end = min(len(lines), call_line + 5)
            
            for i in range(start, end):
                line_num = i + 1
                line_content = lines[i].rstrip()
                
                if line_num == call_line:
                    print(f">>> {line_num:3d}: {line_content}")
                    print(f"     ^^ AQUÍ AGREGAR DEBUG ANTES ^^")
                else:
                    print(f"    {line_num:3d}: {line_content}")
                    
        if not found_calls:
            print("❌ No se encontraron llamadas a generate_response")
            print("🔍 Buscando variaciones...")
            
            # Buscar otras posibles llamadas
            for i, line in enumerate(lines, 1):
                if 'generate_' in line:
                    print(f"   Línea {i}: {line.strip()}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

def show_debug_instructions():
    """
    Mostrar instrucciones claras de dónde agregar el debug
    """
    print(f"\n🔧 INSTRUCCIONES PARA AGREGAR DEBUG:")
    print("="*60)
    print("1. Busca las líneas marcadas con >>> en el resultado anterior")
    print("2. JUSTO ANTES de esa línea, agrega:")
    print()
    print("# 🚨 DEBUG - Ver datos antes de Claude")
    print("print(f'DEBUG: rows={len(rows) if rows else 0}')")
    print("if rows and isinstance(rows[0], dict):")
    print("    print(f'DEBUG: keys={list(rows[0].keys())}')")
    print("    if 'inversion_total_usd' in rows[0]:")
    print("        print(f'DEBUG: inversión=${rows[0][\"inversion_total_usd\"]:,.2f}')")
    print("    else:")
    print("        print('DEBUG: NO HAY inversion_total_usd')")
    print()

if __name__ == "__main__":
    find_generate_response_calls()
    show_debug_instructions()

