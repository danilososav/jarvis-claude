"""
TEST DEL ERROR DE BD SIN CLAUDE API
Simula el flujo completo hasta el punto de guardado en BD
"""

import sys
import os
sys.path.append('.')
import json
from datetime import datetime

def test_bd_error_simulation():
    """
    Simula exactamente lo que hace el endpoint /api/query hasta el guardado
    """
    print("🧪 TEST SIMULACIÓN ERROR BD")
    print("="*50)
    
    try:
        # Importar clases necesarias
        import app
        from app import Session, Conversation
        
        # SIMULAR DATOS EXACTOS que genera el endpoint
        user_id = 1
        session_id = "test_session"
        user_query = "cervepar cuanto facturo y cuanto invirtio en tv"
        query_type = "facturacion"
        
        # SIMULAR datos formateados (lo que retorna get_facturacion_enriched + format_data_for_claude)
        rows = [{
            'cliente': 'CERVEPAR S.A.',
            'facturacion': 27757329015.25,
            'promedio_mensual': 18554364.32,
            'market_share': 14.69,
            'inversion_detalle': [
                {'medio': 'TV ABERTA', 'inversion_usd': 33565.31},
                {'medio': 'TV ASSINATURA', 'inversion_usd': 5678.96}
            ],
            'inversion_total_usd': 39244.27,
            'ranking': 7,
            'aporte_dnit': 207373000000
        }]
        
        # SIMULAR respuesta de Claude (sin llamar a la API)
        mock_claude_response = """CERVEPAR S.A. facturó un total de 27.757.329.015 Gs con un promedio mensual de 18.554.364 Gs, e invirtió $39.244,27 USD en televisión durante el período analizado.

La empresa ocupa una posición sólida en el mercado publicitario paraguayo con un market share del 14,69%, lo que la posiciona como uno de los anunciantes más relevantes del país."""
        
        # SIMULAR construcción de responses (como hace el endpoint)
        responses = []
        
        # Simular intención "text_only"
        responses.append({
            "type": "text",
            "content": mock_claude_response,
            "query_type": query_type,
            "data": rows
        })
        
        print("✅ Datos simulados:")
        print(f"   user_id: {user_id}")
        print(f"   session_id: {session_id}")
        print(f"   user_query: {user_query}")
        print(f"   query_type: {query_type}")
        print(f"   rows: {len(rows)} registros")
        print(f"   responses: {len(responses)} respuestas")
        
        # 🚨 DEBUG ANTES DEL GUARDADO (igual que en app.py)
        print(f"\n🔍 DEBUG BD - ANTES DE GUARDAR:")
        print(f"   responses type: {type(responses)}")
        print(f"   responses length: {len(responses) if responses else 0}")
        
        if responses:
            for i, resp in enumerate(responses):
                print(f"   response[{i}]: {type(resp)} - {list(resp.keys()) if isinstance(resp, dict) else 'no keys'}")
        else:
            print("   ❌ responses está vacío!")
        
        # SIMULAR GUARDADO EN BD (igual que en app.py)
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
            
            print(f"   ✅ Conversación guardada: {conversation.id}")
            session.close()
            
        except Exception as e:
            print(f"   ❌ ERROR ESPECÍFICO: {e}")
            print(f"   ❌ ERROR TIPO: {type(e)}")
            import traceback
            traceback.print_exc()
            
            # Mostrar más detalles del error
            print(f"\n🔍 ANÁLISIS DEL ERROR:")
            if "list index out of range" in str(e):
                print("   → Error: acceso a lista vacía")
                print("   → Verificar que responses[] tenga elementos")
            elif "IntegrityError" in str(e):
                print("   → Error: violación de restricción de BD")
                print("   → Verificar campos requeridos")
            elif "AttributeError" in str(e):
                print("   → Error: atributo faltante")
                print("   → Verificar estructura del objeto")
            
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        print("Asegúrate de ejecutar desde la carpeta del backend")
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bd_error_simulation()

