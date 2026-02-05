"""
DEBUG: Identificar exactamente dónde está el error "list index out of range"
"""

debug_code_bd = '''
# 🚨 DEBUG PARA EL ERROR DE BD - AGREGAR ANTES DEL GUARDADO

print(f"🔍 DEBUG BD - ANTES DE GUARDAR:")
print(f"   responses type: {type(responses)}")
print(f"   responses length: {len(responses) if responses else 0}")
print(f"   responses content: {responses}")

if responses:
    for i, resp in enumerate(responses):
        print(f"   response[{i}]: {type(resp)} - {list(resp.keys()) if isinstance(resp, dict) else 'no keys'}")
else:
    print("   ❌ responses está vacío!")

# GUARDAR EN BD (solo la primera respuesta para historial)
try:
    session = Session()
    
    # ✅ VALIDACIÓN MEJORADA
    if responses and len(responses) > 0:
        main_response = responses[0]
        print(f"   ✅ main_response: {type(main_response)}")
        print(f"   ✅ main_response keys: {list(main_response.keys()) if isinstance(main_response, dict) else 'no keys'}")
    else:
        main_response = {"type": "text", "content": "Sin respuesta"}
        print(f"   ⚠️ usando main_response por defecto")
    
    print(f"   ✅ Creando conversation object...")
    
    conversation = Conversation(
        user_id=user_id,
        session_id=session_id,
        query=user_query,
        response=main_response.get("content", ""),
        query_type=query_type,
        chart_config=json.dumps(main_response.get("chart_config")) if main_response.get("chart_config") else None,
        chart_data=json.dumps(rows) if rows else None
    )
    
    print(f"   ✅ Conversation creado, guardando...")
    session.add(conversation)
    session.commit()
    session.close()
    
    print(f"   ✅ Conversación guardada: {conversation.id}")
    
except Exception as e:
    print(f"   ❌ ERROR ESPECÍFICO: {e}")
    print(f"   ❌ ERROR TIPO: {type(e)}")
    import traceback
    traceback.print_exc()
'''

print("🔧 AGREGAR DEBUG AL APP.PY")
print("="*50)
print("Busca en app.py la sección:")
print("   # GUARDAR EN BD (solo la primera respuesta para historial)")
print()
print("Y REEMPLAZA toda esa sección con:")
print()
print(debug_code_bd)
print()
print("Esto va a mostrar EXACTAMENTE dónde está el problema.")

def possible_fixes():
    """
    Posibles arreglos según el tipo de error
    """
    print(f"\n🔧 POSIBLES ARREGLOS:")
    print("="*30)
    
    print("1️⃣ Si responses está vacío:")
    print("   → El problema está en la construcción de responses[]")
    print("   → Verificar que responses.append() se ejecute correctamente")
    
    print(f"\n2️⃣ Si responses[0] no tiene 'content':")
    print("   → Cambiar main_response.get('content', '') por main_response.get('content', 'Sin contenido')")
    
    print(f"\n3️⃣ Si el error está en Conversation():")
    print("   → Problema con los parámetros del objeto")
    print("   → Verificar que todos los campos requeridos estén presentes")
    
    print(f"\n4️⃣ Si el error está en session.add():")
    print("   → Problema con la estructura de la tabla")
    print("   → Verificar que la tabla conversations existe")

if __name__ == "__main__":
    print("🎯 OBJETIVO: Identificar el error 'list index out of range'")
    print("="*60)
    print("✅ Claude funciona perfecto")
    print("✅ Respuesta generada correctamente") 
    print("❌ Error al guardar en BD")
    print()
    possible_fixes()

