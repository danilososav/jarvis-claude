"""
Ver contexto específico de la línea 899 - el verdadero culpable
"""

def show_line_899_context():
    """
    Mostrar 10 líneas antes y después de la línea 899
    """
    print("🔍 CONTEXTO DE LÍNEA 899 - EL CULPABLE")
    print("="*50)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Mostrar contexto alrededor de línea 899
        target_line = 899
        start = max(0, target_line - 10)
        end = min(len(lines), target_line + 10)
        
        print(f"Mostrando líneas {start+1} a {end}:")
        print("-" * 60)
        
        for i in range(start, end):
            line_num = i + 1
            line_content = lines[i].rstrip()
            
            if line_num == target_line:
                print(f">>> {line_num:3d}: {line_content}")
                print("     ^^^ ESTA ES LA LÍNEA DEL ERROR ^^^")
            else:
                print(f"    {line_num:3d}: {line_content}")
                
        # Buscar todas las líneas donde se modifica responses
        print(f"\n🔍 TODAS LAS MODIFICACIONES A responses[]:")
        print("-" * 50)
        
        for i, line in enumerate(lines, 1):
            line_strip = line.strip()
            if 'responses' in line_strip and ('append' in line_strip or 'responses =' in line_strip):
                print(f"   Línea {i}: {line_strip}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def show_fix():
    """
    Mostrar el arreglo específico para línea 899
    """
    print(f"\n🔧 ARREGLO PARA LÍNEA 899:")
    print("="*40)
    print("Busca en app.py línea 899:")
    print("   main_response = responses[0]")
    print()
    print("Y CÁMBIALA por:")
    print("   main_response = responses[0] if responses and len(responses) > 0 else {'type': 'text', 'content': 'Sin respuesta'}")
    print()
    print("O mejor aún, usa este bloque:")
    print("   if responses and len(responses) > 0:")
    print("       main_response = responses[0]")
    print("   else:")
    print("       main_response = {'type': 'text', 'content': 'Sin respuesta'}")
    print("       print('⚠️ responses está vacío en línea 899')")

if __name__ == "__main__":
    show_line_899_context()
    show_fix()

