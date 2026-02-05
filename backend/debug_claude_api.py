"""
DEBUG FINAL: Interceptar qué datos recibe exactamente Claude API
"""

# Crear parche temporal para interceptar llamadas a Claude
import json
import sys
import os

def patch_claude_handler():
    """
    Parcheamos temporalmente el ClaudeHandler para ver qué datos recibe
    """
    print("🔧 APLICANDO PARCHE TEMPORAL A CLAUDE HANDLER")
    print("="*60)
    
    try:
        # Leer el archivo claude_handler_v2.py
        if os.path.exists('claude_handler_v2.py'):
            with open('claude_handler_v2.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar la función enhance_response
            if 'def enhance_response(' in content:
                print("✅ Encontrado claude_handler_v2.py")
                
                # Crear versión patcheada
                patched_content = content.replace(
                    'def enhance_response(',
                    '''def enhance_response_original(self, user_query, data, query_type):
        """Función original renombrada"""
        
    def enhance_response('''
                )
                
                # Agregar función de debug al principio de enhance_response
                debug_code = '''
        """
        🚨 DEBUG: Interceptar datos que llegan a Claude
        """
        print("\\n🔍 CLAUDE API - DATOS RECIBIDOS:")
        print("="*50)
        print(f"user_query: {user_query}")
        print(f"query_type: {query_type}")
        print(f"data type: {type(data)}")
        print(f"data length: {len(data) if data else 0}")
        
        if data:
            print(f"\\n📋 DATOS DETALLADOS:")
            for i, row in enumerate(data):
                print(f"  Row {i+1}: {type(row)}")
                if isinstance(row, dict):
                    print(f"    Keys: {list(row.keys())}")
                    if 'cliente' in row:
                        print(f"    Cliente: {row.get('cliente')}")
                    if 'facturacion' in row:
                        print(f"    Facturación: {row.get('facturacion'):,.0f}")
                    if 'inversion_total_usd' in row:
                        print(f"    Inversión USD: ${row.get('inversion_total_usd'):,.2f}")
                        print(f"    🚨 CLAUDE VE LA INVERSIÓN: {row.get('inversion_total_usd', 0) > 0}")
                    if 'ranking' in row:
                        print(f"    Ranking: #{row.get('ranking')}")
        print("="*50)
        
        # Llamar función original
        return self.enhance_response_original(user_query, data, query_type)'''
                
                # Insertar el debug code después de def enhance_response
                patched_content = patched_content.replace(
                    'def enhance_response(self, user_query, data, query_type):',
                    f'def enhance_response(self, user_query, data, query_type):{debug_code}'
                )
                
                # Guardar versión patcheada
                with open('claude_handler_v2_debug.py', 'w', encoding='utf-8') as f:
                    f.write(patched_content)
                
                print("✅ Claude handler patcheado guardado como claude_handler_v2_debug.py")
                print("🔧 Ahora necesitas:")
                print("   1. Parar Flask")
                print("   2. Reemplazar: cp claude_handler_v2_debug.py claude_handler_v2.py")
                print("   3. Reiniciar Flask")
                print("   4. Hacer una consulta")
                print("   5. Ver en consola qué datos recibe Claude")
                
            else:
                print("❌ No se encontró enhance_response en claude_handler_v2.py")
                
        else:
            print("❌ No se encontró claude_handler_v2.py")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def alternative_debug():
    """
    Alternativa: agregar debug directo al app.py antes de generate_response
    """
    print(f"\\n🔧 ALTERNATIVA: AGREGAR DEBUG AL APP.PY")
    print("-" * 40)
    print("Agrega estas líneas antes de la llamada a generate_response():")
    print()
    print("```python")
    print("# 🚨 DEBUG TEMPORAL - Verificar datos antes de Claude")
    print("logger.info(f'🔍 DEBUG: query_type={query_type}, rows={len(rows)}')")
    print("if rows:")
    print("    logger.info(f'🔍 DEBUG: row[0] keys={list(rows[0].keys())}')")
    print("    if isinstance(rows[0], dict) and 'inversion_total_usd' in rows[0]:")
    print("        logger.info(f'🔍 DEBUG: inversion_total_usd={rows[0][\"inversion_total_usd\"]}')")
    print("        logger.info(f'🔍 DEBUG: CLAUDE DEBERÍA VER INVERSIÓN: {rows[0][\"inversion_total_usd\"] > 0}')")
    print("```")

if __name__ == "__main__":
    patch_claude_handler()
    alternative_debug()

