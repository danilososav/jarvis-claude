"""
Test de Claude Handler
Valida que Claude API funciona correctamente
"""

from claude_handler_v2 import ClaudeHandler
import os
from dotenv import load_dotenv

load_dotenv()

def test_claude():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY no encontrada en .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...")
    
    # Inicializar handler
    try:
        handler = ClaudeHandler(api_key)
        print("✅ ClaudeHandler inicializado")
    except Exception as e:
        print(f"❌ Error inicializando: {e}")
        return False
    
    # Test 1: Ranking simple
    print("\n=== TEST 1: Ranking ===")
    data_ranking = [
        {"cliente": "CERVEPAR", "facturacion": 21228763493.72, "market_share": 7.89, "registros": 120},
        {"cliente": "UNILEVER", "facturacion": 15847392847.32, "market_share": 5.89, "registros": 98},
        {"cliente": "COCA COLA", "facturacion": 12394857432.11, "market_share": 4.61, "registros": 85}
    ]
    
    try:
        response = handler.enhance_response(
            user_query="dame el top 3 de clientes",
            data=data_ranking,
            query_type="ranking"
        )
        print("Respuesta de Claude:")
        print(response)
        print("\n✅ Test 1 exitoso")
    except Exception as e:
        print(f"❌ Error en test 1: {e}")
        return False
    
    # Test 2: Facturación específica
    print("\n=== TEST 2: Facturación Específica ===")
    data_fac = [
        {
            "cliente": "CERVEPAR",
            "facturacion": 21228763493.72,
            "promedio_mensual": 1768980291.14,
            "market_share": 7.89,
            "registros": 120
        }
    ]
    
    try:
        response = handler.enhance_response(
            user_query="cuanto facturo cervepar",
            data=data_fac,
            query_type="facturacion"
        )
        print("Respuesta de Claude:")
        print(response)
        print("\n✅ Test 2 exitoso")
    except Exception as e:
        print(f"❌ Error en test 2: {e}")
        return False
    
    # Test 3: Query paraguayo coloquial
    print("\n=== TEST 3: Query Paraguayo Coloquial ===")
    try:
        response = handler.enhance_response(
            user_query="che dame nomás los clientes que más facturan",
            data=data_ranking,
            query_type="ranking"
        )
        print("Respuesta de Claude:")
        print(response)
        print("\n✅ Test 3 exitoso")
    except Exception as e:
        print(f"❌ Error en test 3: {e}")
        return False
    
    print("\n" + "="*50)
    print("✅ TODOS LOS TESTS EXITOSOS")
    print("="*50)
    return True

if __name__ == "__main__":
    test_claude()
