"""
TEST DE COBERTURA DE CLIENTES SIN CLAUDE API
Verificar qué clientes están disponibles y funcionan en el sistema
"""

import sys
import os
sys.path.append('.')

def test_client_coverage():
    """
    Probar diferentes clientes para verificar cobertura del sistema
    """
    print("🧪 TEST COBERTURA DE CLIENTES")
    print("="*60)
    
    try:
        # Importar funciones necesarias
        import app
        from app import get_facturacion_enriched, format_data_for_claude
        
        # Lista de clientes para probar
        test_clients = [
            "telefonica",
            "unilever", 
            "nestle",
            "coca cola",
            "tigo",
            "personal",
            "copetrol",
            "banco nacional",
            "banco continental",
            "cerveza brahma",
            "pilsen",
            "pizza hut",
            "mcdonalds",
            "carrefour",
            "stock center"
        ]
        
        print(f"🔍 PROBANDO {len(test_clients)} CLIENTES:")
        print("-" * 50)
        
        results = {
            'encontrados': [],
            'sin_datos': [],
            'con_inversion': [],
            'solo_facturacion': [],
            'errores': []
        }
        
        for cliente in test_clients:
            print(f"\n🏢 PROBANDO: {cliente}")
            
            try:
                # Test 1: get_facturacion_enriched
                query_test = f"{cliente} cuanto facturo"
                rows = get_facturacion_enriched(query_test)
                
                if not rows:
                    print(f"   ❌ No encontrado en BD")
                    results['sin_datos'].append(cliente)
                    continue
                
                print(f"   ✅ Encontrado: {rows[0].get('cliente', 'Sin nombre')}")
                results['encontrados'].append(cliente)
                
                # Test 2: format_data_for_claude
                formatted = format_data_for_claude(rows, 'facturacion')
                
                if not formatted:
                    print(f"   ⚠️ Error en format_data_for_claude")
                    results['errores'].append(cliente)
                    continue
                
                # Test 3: Verificar datos disponibles
                client_data = formatted[0]
                facturacion = client_data.get('facturacion', 0)
                inversion = client_data.get('inversion_total_usd', 0)
                ranking = client_data.get('ranking', None)
                
                print(f"   💰 Facturación: {facturacion:,.0f} Gs")
                
                if inversion > 0:
                    print(f"   📺 Inversión TV: ${inversion:,.2f} USD")
                    if 'inversion_detalle' in client_data:
                        detalle = client_data['inversion_detalle']
                        print(f"   📊 Detalle: {len(detalle)} medios")
                    results['con_inversion'].append(cliente)
                else:
                    print(f"   📺 Sin inversión TV registrada")
                    results['solo_facturacion'].append(cliente)
                
                if ranking:
                    print(f"   🏆 Ranking DNIT: #{ranking}")
                else:
                    print(f"   🏆 Sin ranking DNIT")
                
                # Test 4: Simular respuesta
                if inversion > 0:
                    mock_response = f"{client_data['cliente']} facturó {facturacion:,.0f} Gs e invirtió ${inversion:,.2f} USD en televisión."
                else:
                    mock_response = f"{client_data['cliente']} facturó {facturacion:,.0f} Gs. Sin datos de inversión en televisión."
                
                print(f"   💬 Respuesta simulada: {mock_response[:80]}...")
                
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                results['errores'].append(cliente)
        
        # RESUMEN DE RESULTADOS
        print(f"\n📊 RESUMEN DE COBERTURA:")
        print("="*50)
        print(f"📈 CLIENTES ENCONTRADOS: {len(results['encontrados'])}/{len(test_clients)}")
        print(f"💎 Con datos completos: {len(results['con_inversion'])}")
        print(f"💰 Solo facturación: {len(results['solo_facturacion'])}")
        print(f"❌ Sin datos: {len(results['sin_datos'])}")
        print(f"🚨 Errores: {len(results['errores'])}")
        
        if results['con_inversion']:
            print(f"\n✅ CLIENTES CON DATOS COMPLETOS:")
            for cliente in results['con_inversion']:
                print(f"   • {cliente}")
        
        if results['solo_facturacion']:
            print(f"\n⚠️ CLIENTES SOLO FACTURACIÓN:")
            for cliente in results['solo_facturacion']:
                print(f"   • {cliente}")
        
        if results['sin_datos']:
            print(f"\n❌ CLIENTES NO ENCONTRADOS:")
            for cliente in results['sin_datos']:
                print(f"   • {cliente}")
        
        if results['errores']:
            print(f"\n🚨 CLIENTES CON ERRORES:")
            for cliente in results['errores']:
                print(f"   • {cliente}")
        
        # ANÁLISIS DE COBERTURA
        total_encontrados = len(results['encontrados'])
        if total_encontrados > 0:
            pct_completos = (len(results['con_inversion']) / total_encontrados) * 100
            pct_parciales = (len(results['solo_facturacion']) / total_encontrados) * 100
            
            print(f"\n🎯 ANÁLISIS:")
            print("="*30)
            print(f"📊 {pct_completos:.1f}% con datos completos (facturación + inversión)")
            print(f"📊 {pct_parciales:.1f}% con datos parciales (solo facturación)")
            
            if pct_completos >= 70:
                print("✅ COBERTURA EXCELENTE - Sistema funciona para mayoría")
            elif pct_completos >= 40:
                print("⚠️ COBERTURA BUENA - Funciona para casos principales")
            else:
                print("❌ COBERTURA LIMITADA - Necesita mejoras en fuzzy matching")
        
        return results
        
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        return None
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_fuzzy_matching():
    """
    Test específico de fuzzy matching con variaciones de nombres
    """
    print(f"\n🔍 TEST FUZZY MATCHING:")
    print("="*40)
    
    # Casos de fuzzy matching
    fuzzy_tests = [
        ("telefonica", "TELECOM PERSONAL S.A."),
        ("personal", "TELECOM PERSONAL S.A."), 
        ("tigo", "TIGO PARAGUAY S.A."),
        ("coca", "COCA COLA FEMSA S.A."),
        ("coca cola", "COCA COLA FEMSA S.A."),
        ("unilever", "UNILEVER DE PARAGUAY S.A."),
        ("nestle", "NESTLE PARAGUAY S.A."),
        ("banco nacional", "BANCO NACIONAL DE FOMENTO"),
        ("copetrol", "PETROPAR - COPETROL")
    ]
    
    try:
        from app import get_facturacion_enriched
        
        for query_name, expected_name in fuzzy_tests:
            print(f"\n🔎 '{query_name}' → buscando '{expected_name}'")
            
            rows = get_facturacion_enriched(f"{query_name} facturacion")
            
            if rows:
                found_name = rows[0].get('cliente', '')
                print(f"   ✅ Encontrado: {found_name}")
                
                # Verificar si el match es correcto
                if expected_name.lower() in found_name.lower() or found_name.lower() in expected_name.lower():
                    print(f"   ✅ Match correcto")
                else:
                    print(f"   ⚠️ Match diferente al esperado")
            else:
                print(f"   ❌ No encontrado")
                
    except Exception as e:
        print(f"❌ Error en fuzzy test: {e}")

if __name__ == "__main__":
    print("🎯 OBJETIVO: Verificar cobertura de clientes sin gastar créditos")
    print("="*70)
    print("✅ Test completo del pipeline de datos")
    print("✅ Sin llamadas a Claude API") 
    print("✅ Verificar fuzzy matching")
    print()
    
    # Test principal
    results = test_client_coverage()
    
    # Test fuzzy matching
    test_fuzzy_matching()
    
    if results:
        total_success = len(results['encontrados'])
        total_tests = len(results['encontrados']) + len(results['sin_datos']) + len(results['errores'])
        
        print(f"\n🎯 RESULTADO FINAL:")
        print("="*40)
        print(f"📊 Cobertura: {total_success}/{total_tests} clientes ({(total_success/total_tests*100):.1f}%)")
        
        if total_success >= 10:
            print("🎉 SISTEMA LISTO - Buena cobertura de clientes")
            print("✅ Puede responder consultas de múltiples anunciantes")
        elif total_success >= 5:
            print("⚠️ COBERTURA PARCIAL - Funciona para clientes principales")
            print("🔧 Considera mejorar fuzzy matching para más cobertura")
        else:
            print("❌ COBERTURA LIMITADA - Revisar configuración BD")

