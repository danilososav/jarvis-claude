"""
DEBUG: Interceptar el prompt exacto que se envía a Claude API
"""

import os

def patch_claude_handler():
    """
    Parchear claude_handler_v2.py para ver el prompt exacto
    """
    print("🔍 INTERCEPTANDO PROMPT A CLAUDE API")
    print("="*50)
    
    try:
        # Leer claude_handler_v2.py
        with open('claude_handler_v2.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar la construcción del prompt
        lines = content.split('\n')
        
        patched_lines = []
        for line in lines:
            # Agregar debug antes de enviar a Claude
            if 'messages=' in line and 'anthropic' in content.lower():
                # Agregar debug
                indent = len(line) - len(line.lstrip())
                debug_code = ' ' * indent + "print(f'🔍 PROMPT A CLAUDE: {messages}')"
                patched_lines.append(debug_code)
                
            # También interceptar donde se construye el prompt de usuario
            if 'role": "user"' in line or "'user'" in line:
                indent = len(line) - len(line.lstrip()) 
                debug_code = ' ' * indent + "print(f'🔍 USER PROMPT: {content if \"content\" in locals() else \"content not found\"}')"
                patched_lines.append(debug_code)
                
            patched_lines.append(line)
            
        # Guardar versión patcheada
        with open('claude_handler_v2_debug.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(patched_lines))
            
        print("✅ Claude handler debug creado")
        print("🔧 Para activar:")
        print("   1. cp claude_handler_v2_debug.py claude_handler_v2.py")
        print("   2. Habilitar ANTHROPIC_API_KEY en .env")
        print("   3. Reiniciar Flask")
        print("   4. Hacer consulta")
        print("   5. Ver prompt exacto en consola")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def alternative_simple_debug():
    """
    Alternativa más simple: agregar debug directo
    """
    print(f"\n🔧 ALTERNATIVA SIMPLE:")
    print("-" * 30)
    print("Agrega esta línea en claude_handler_v2.py en el método enhance_response:")
    print()
    print("```python")
    print("def enhance_response(self, user_query, data, query_type):")
    print("    # 🚨 DEBUG")
    print("    print(f'CLAUDE RECIBE: query={user_query}, data={data}, query_type={query_type}')")
    print("    # ... resto del código")
    print("```")

def show_current_findings():
    """
    Mostrar lo que hemos confirmado
    """
    print(f"\n✅ LO QUE CONFIRMAMOS:")
    print("="*50)
    print("✅ get_facturacion_enriched() funciona")
    print("✅ format_data_for_claude() funciona") 
    print("✅ Los datos llegan con inversion_total_usd=$39,244.27")
    print("✅ Claude API recibe los datos correctos")
    print()
    print("❓ LO QUE FALTA VERIFICAR:")
    print("="*30)
    print("❓ ¿Cómo se construye el prompt en claude_handler_v2.py?")
    print("❓ ¿El prompt incluye los datos de inversión?")
    print("❓ ¿Claude interpreta mal el prompt?")
    print()
    print("🎯 PRÓXIMO PASO:")
    print("="*20) 
    print("1. Habilitar ANTHROPIC_API_KEY")
    print("2. Agregar debug al claude_handler_v2.py")
    print("3. Ver qué prompt exacto se envía a Claude")
    print("4. UNA consulta para diagnosticar")

if __name__ == "__main__":
    show_current_findings()
    patch_claude_handler()
    alternative_simple_debug()

