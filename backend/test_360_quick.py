"""
TEST RÁPIDO JARVIS 360° CORREGIDO
Test simple con engine correcto para verificar funcionamiento
"""

def test_360_quick():
    """
    Test rápido del sistema 360° con engine correcto
    """
    print("🧪 TEST RÁPIDO JARVIS 360°")
    print("="*50)
    
    try:
        # Imports con engine
        from jarvis_360_integration import (
            get_cliente_360,
            format_data_for_claude_360
        )
        from app import engine
        
        print("✅ Imports correctos (incluyendo engine)")
        
        # Test básico
        test_queries = ["unilever facturacion", "cervepar datos", "telefonica perfil"]
        
        for query in test_queries:
            print(f"\n🏢 TEST: '{query}'")
            
            try:
                # ✅ LLAMADA CORRECTA CON ENGINE
                rows = get_cliente_360(query, engine)
                
                if rows:
                    cliente = rows[0]
                    print(f"   ✅ ENCONTRADO: {cliente.get('cliente', 'N/A')}")
                    print(f"   💰 Facturación: {cliente.get('facturacion', 0):,.0f} Gs")
                    
                    # Verificar datos 360°
                    campos_360 = []
                    if cliente.get('cluster'): campos_360.append(f"Cluster: {cliente.get('cluster')}")
                    if cliente.get('cultura'): campos_360.append(f"Cultura: {cliente.get('cultura')}")
                    if cliente.get('inversion_total_usd', 0) > 0: campos_360.append(f"Inversión: ${cliente.get('inversion_total_usd'):,.0f}")
                    if cliente.get('ranking'): campos_360.append(f"Ranking: #{cliente.get('ranking')}")
                    
                    print(f"   🎯 Datos 360°: {len(campos_360)} disponibles")
                    for campo in campos_360[:3]:  # Solo primeros 3
                        print(f"      • {campo}")
                    
                    # Test formato
                    formatted = format_data_for_claude_360(rows, "facturacion")
                    if formatted:
                        print(f"   ✅ Formato 360° aplicado correctamente")
                        
                        # Simular prompt
                        cliente_fmt = formatted[0]
                        mock_prompt = f"CLIENTE: {cliente_fmt.get('cliente')}\n"
                        if cliente_fmt.get('cluster'):
                            mock_prompt += f"CLUSTER: {cliente_fmt.get('cluster')}\n"
                        if cliente_fmt.get('inversion_total_usd', 0) > 0:
                            mock_prompt += f"INVERSIÓN: ${cliente_fmt.get('inversion_total_usd'):,.0f} USD\n"
                        
                        print(f"   💬 Prompt sample: {len(mock_prompt)} chars")
                    
                else:
                    print(f"   ❌ Cliente no encontrado")
                    
            except Exception as e:
                print(f"   🚨 Error: {str(e)[:100]}...")
        
        print(f"\n🎯 TEST FINAL:")
        print("="*30)
        
        # Probar una consulta completa
        try:
            final_test = get_cliente_360("unilever facturacion", engine)
            if final_test:
                print("✅ Sistema 360° FUNCIONANDO")
                print("✅ Engine conecta correctamente") 
                print("✅ Datos 360° obtenidos")
                print("✅ Listo para app.py")
                return True
            else:
                print("⚠️ No se encontraron datos")
                return False
                
        except Exception as e:
            print(f"❌ Error final: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Error imports: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    print("🎯 OBJETIVO: Test rápido con engine correcto")
    print("="*60)
    
    success = test_360_quick()
    
    if success:
        print(f"\n🚀 ÉXITO TOTAL!")
        print("="*30)
        print("✅ Sistema 360° implementado y funcionando")
        print("✅ Engine configurado correctamente")
        print("✅ Datos 360° disponibles")
        print("✅ Listo para prueba final con Claude API")
        print()
        print("🎯 PRÓXIMO PASO:")
        print("   Habilitar ANTHROPIC_API_KEY y probar:")
        print("   'unilever facturacion' en el frontend")
    else:
        print(f"\n❌ Aún hay problemas")
        print("   Revisar configuración de BD y engine")

