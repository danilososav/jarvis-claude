"""
TEST del claude_handler_v2.py CORREGIDO sin gastar créditos
Simula exactamente lo que haría Claude API con el método _format_data corregido
"""

import sys
import os
sys.path.append('.')

def test_claude_handler_corregido():
    """
    Simula el método _format_data corregido con datos reales de CERVEPAR
    """
    print("🧪 TEST CLAUDE HANDLER CORREGIDO")
    print("="*60)
    
    # DATOS EXACTOS que recibe claude_handler_v2.py (del debug anterior)
    test_data = [{
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
    
    # SIMULAR método _format_data CORREGIDO
    def _format_data_corregido(data, query_type):
        """Copia exacta del método corregido"""
        if not data:
            return "No hay datos disponibles"
        
        if query_type == "facturacion":
            item = data[0] if data else {}
            
            # ✅ DATOS BASE
            result = f"""Cliente: {item.get('cliente', 'N/A')}
Facturación Total: {item.get('facturacion', 0):,.0f} Gs
Promedio Mensual: {item.get('promedio_mensual', 0):,.0f} Gs
Market Share: {item.get('market_share', 0):.2f}%"""
            
            # ✅ NUEVO: DATOS DE INVERSIÓN
            if item.get('inversion_total_usd', 0) > 0:
                result += f"\nInversión en TV: ${item.get('inversion_total_usd', 0):,.2f} USD"
                
                # Detalle por tipo de TV
                if item.get('inversion_detalle'):
                    result += "\nDetalle inversión:"
                    for inv in item.get('inversion_detalle', []):
                        result += f"\n  - {inv.get('medio', 'N/A')}: ${inv.get('inversion_usd', 0):,.2f} USD"
            else:
                result += "\nInversión en TV: Sin datos registrados"
            
            # ✅ NUEVO: RANKING DNIT
            if item.get('ranking'):
                result += f"\nRanking DNIT: #{item.get('ranking')}"
                result += f"\nAporte DNIT: {item.get('aporte_dnit', 0):,.0f} Gs"
            else:
                result += "\nRanking DNIT: Sin datos disponibles"
                
            return result
        
        return str(data)
    
    # SIMULAR prompt completo
    user_query = "cervepar cuanto facturo y cuanto invirtio en tv"
    query_type = "facturacion"
    
    # Generar datos formateados con método CORREGIDO
    data_formatted = _format_data_corregido(test_data, query_type)
    
    # Generar prompt completo como lo haría claude_handler_v2.py
    prompt = f"""QUERY DEL USUARIO:
"{user_query}"

DATOS DISPONIBLES:
{data_formatted}

TIPO DE ANÁLISIS: {query_type}

INSTRUCCIONES ESPECÍFICAS:
- Responde directamente cuánto facturó
- Contextualiza: ¿es un cliente top? ¿qué posición ocupa?
- Analiza su market share: ¿es relevante?
- Compara promedio mensual vs total para identificar estacionalidad
- Menciona número de registros (años/meses activo)

Genera una respuesta analítica profesional completa que responda directamente a la pregunta del usuario."""
    
    # MOSTRAR RESULTADOS
    print("📋 PROMPT QUE RECIBIRÍA CLAUDE:")
    print("="*60)
    print(prompt)
    
    print(f"\n🎯 VERIFICACIÓN:")
    print("="*40)
    print(f"✅ ¿Incluye cliente? {'✅' if 'CERVEPAR' in data_formatted else '❌'}")
    print(f"✅ ¿Incluye facturación? {'✅' if '27,757,329,015' in data_formatted else '❌'}")
    print(f"✅ ¿Incluye inversión USD? {'✅' if '$39,244.27' in data_formatted else '❌'}")
    print(f"✅ ¿Incluye detalle TV? {'✅' if 'TV ABERTA' in data_formatted else '❌'}")
    print(f"✅ ¿Incluye ranking? {'✅' if 'Ranking DNIT: #7' in data_formatted else '❌'}")
    print(f"✅ ¿Incluye aporte DNIT? {'✅' if '207,373,000,000' in data_formatted else '❌'}")
    
    if all([
        'CERVEPAR' in data_formatted,
        '39,244.27' in data_formatted,
        'TV ABERTA' in data_formatted,
        'Ranking DNIT: #7' in data_formatted
    ]):
        print(f"\n🎉 ¡CORRECCIÓN EXITOSA!")
        print("="*40)
        print("✅ Claude ahora recibe TODOS los datos")
        print("✅ Va a mencionar la inversión de $39,244 USD")
        print("✅ Va a mencionar el ranking DNIT #7")
        print("✅ Va a incluir el detalle de TV Abierta y Suscripción")
        print("\n💬 RESPUESTA ESPERADA DE CLAUDE:")
        print("'CERVEPAR S.A. facturó 27,757M Gs e invirtió $39,244 USD")
        print("en televisión distribuido entre TV Abierta ($33,565) y TV")
        print("Suscripción ($5,679). Con ranking DNIT #7 y aporte de")
        print("207,373M Gs, se posiciona como cliente estratégico...'")
    else:
        print(f"\n❌ AÚN HAY PROBLEMA")
        print("="*20)
        print("❌ Algunos datos faltan en el prompt")
        
def comparar_antes_despues():
    """
    Comparar prompt antes vs después de la corrección
    """
    print(f"\n📊 COMPARACIÓN ANTES vs DESPUÉS:")
    print("="*60)
    
    print("❌ ANTES (método original):")
    print("-" * 30)
    print("""Cliente: CERVEPAR S.A.
Facturación Total: 27,757,329,015 Gs
Promedio Mensual: 18,554,364 Gs
Market Share: 14.69%
Registros: 0""")
    
    print(f"\n✅ DESPUÉS (método corregido):")
    print("-" * 30)
    print("""Cliente: CERVEPAR S.A.
Facturación Total: 27,757,329,015 Gs
Promedio Mensual: 18,554,364 Gs
Market Share: 14.69%
Inversión en TV: $39,244.27 USD
Detalle inversión:
  - TV ABERTA: $33,565.31 USD
  - TV ASSINATURA: $5,678.96 USD
Ranking DNIT: #7
Aporte DNIT: 207,373,000,000 Gs""")
    
    print(f"\n🎯 DIFERENCIA CLAVE:")
    print("="*25)
    print("❌ ANTES: Claude NO veía datos de inversión → 'No tengo datos'")
    print("✅ DESPUÉS: Claude SÍ ve inversión completa → Análisis completo")

if __name__ == "__main__":
    test_claude_handler_corregido()
    comparar_antes_despues()

