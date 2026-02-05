"""
Buscar el verdadero culpable del error "list index out of range"
"""

import re

def find_list_accesses():
    """
    Buscar todos los accesos [0] en el endpoint /api/query
    """
    print("🔍 BUSCANDO ACCESOS A LISTAS EN APP.PY")
    print("="*50)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Buscar patrones peligrosos
        patterns = [
            r'\[\s*0\s*\]',  # [0]
            r'responses\[0\]',
            r'data\[0\]', 
            r'rows\[0\]',
            r'result\[0\]',
            r'items\[0\]'
        ]
        
        found_issues = []
        
        for i, line in enumerate(lines, 1):
            line_strip = line.strip()
            
            # Buscar accesos [0]
            for pattern in patterns:
                if re.search(pattern, line_strip):
                    found_issues.append({
                        'line': i,
                        'content': line_strip,
                        'pattern': pattern
                    })
        
        print(f"🔍 ENCONTRADOS {len(found_issues)} ACCESOS POTENCIALMENTE PELIGROSOS:")
        print("-" * 60)
        
        # Filtrar solo los del endpoint /api/query
        in_query_endpoint = False
        query_issues = []
        
        for i, line in enumerate(lines, 1):
            line_strip = line.strip()
            
            # Detectar inicio del endpoint query
            if 'def query(' in line_strip:
                in_query_endpoint = True
                start_line = i
                
            # Detectar fin del endpoint (siguiente def o final)
            elif in_query_endpoint and (line_strip.startswith('def ') or line_strip.startswith('@app.route')):
                in_query_endpoint = False
                
            # Si estamos en el endpoint, buscar accesos peligrosos
            elif in_query_endpoint:
                for pattern in patterns:
                    if re.search(pattern, line_strip):
                        query_issues.append({
                            'line': i,
                            'content': line_strip,
                            'pattern': pattern
                        })
        
        if query_issues:
            print(f"🚨 ACCESOS PELIGROSOS EN ENDPOINT /api/query:")
            print("-" * 50)
            for issue in query_issues:
                print(f"   Línea {issue['line']}: {issue['content']}")
                print(f"   Patrón: {issue['pattern']}")
                print()
        else:
            print("✅ No se encontraron accesos peligrosos en /api/query")
            
        # Buscar también accesos sin verificación
        print(f"\n🔍 BUSCANDO ACCESOS SIN VALIDACIÓN:")
        print("-" * 40)
        
        dangerous_lines = []
        for issue in query_issues:
            line_num = issue['line']
            line_content = issue['content']
            
            # Ver líneas anteriores para buscar validación
            context_start = max(0, line_num - 3)
            context_lines = lines[context_start:line_num]
            
            # Buscar if que valide la lista
            has_validation = False
            for ctx_line in context_lines:
                if any(word in ctx_line.lower() for word in ['if', 'len(', 'and', 'or']):
                    has_validation = True
                    break
            
            if not has_validation:
                dangerous_lines.append(issue)
        
        if dangerous_lines:
            print("❌ ACCESOS SIN VALIDACIÓN (CULPABLES PROBABLES):")
            for issue in dangerous_lines:
                print(f"   Línea {issue['line']}: {issue['content']}")
        else:
            print("✅ Todos los accesos tienen validación")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def suggest_fixes():
    """
    Sugerir arreglos para accesos sin validación
    """
    print(f"\n🔧 ARREGLOS SUGERIDOS:")
    print("="*30)
    print("Para cualquier acceso [0] sin validación:")
    print()
    print("❌ PELIGROSO:")
    print("   item = responses[0]")
    print()
    print("✅ SEGURO:")
    print("   if responses and len(responses) > 0:")
    print("       item = responses[0]")
    print("   else:")
    print("       item = {'default': 'value'}")

if __name__ == "__main__":
    print("🎯 OBJETIVO: Encontrar el verdadero error 'list index out of range'")
    print("="*70)
    print("✅ Guardado BD funciona perfectamente")
    print("❌ Error está en otro acceso a lista")
    print()
    
    find_list_accesses()
    suggest_fixes()

