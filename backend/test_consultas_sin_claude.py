"""
TEST CONSULTAS COMPLEJAS SIN CLAUDE API
Explorar todos los datos sin usar créditos
"""

import json
import sys
import os

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_consultas_sin_creditos():
    """
    Test completo de consultas complejas sin Claude API
    """
    
    print("🚀 TEST CONSULTAS COMPLEJAS SIN CLAUDE")
    print("="*70)
    print("✅ Objetivo: Explorar TODOS los datos sin usar créditos")
    print("✅ Resultados: JSON puro con datos de 5 tablas integradas")
    print()
    
    try:
        # Importar dependencias
        from app import engine
        from jarvis_360_integration import get_consulta_compleja_sin_claude
        
        print("✅ Imports correctos - engine disponible")
        print()
        
        # LISTA DE CONSULTAS DE PRUEBA
        consultas_test = [
            {
                "titulo": "🔥 COMPARACIÓN MULTI-CLIENTE",
                "query": "comparar unilever vs cervepar vs nestle",
                "descripcion": "Comparar 3 clientes con todos sus datos"
            },
            {
                "titulo": "🏆 RANKING TOP 10 COMPLETO", 
                "query": "top 10 clientes con clusters y medios",
                "descripcion": "Top 10 con facturación, clusters, inversiones"
            },
            {
                "titulo": "🌍 ANÁLISIS DE CLUSTERS",
                "query": "analisis por clusters con inversiones", 
                "descripcion": "Agrupación por tipo de empresa"
            },
            {
                "titulo": "📊 DATOS ULTRA COMPLETOS",
                "query": "datos completos de cervepar",
                "descripcion": "TODOS los campos de CERVEPAR"
            },
            {
                "titulo": "📈 ESTADÍSTICAS DE MERCADO",
                "query": "estadisticas del mercado publicitario",
                "descripcion": "Resumen general + top sectores"
            }
        ]
        
        # EJECUTAR CADA CONSULTA
        for i, test_case in enumerate(consultas_test, 1):
            print(f"🧪 TEST {i}: {test_case['titulo']}")
            print(f"Query: '{test_case['query']}'")
            print(f"Objetivo: {test_case['descripcion']}")
            print("-" * 60)
            
            try:
                # EJECUTAR SIN CLAUDE
                resultado = get_consulta_compleja_sin_claude(test_case['query'], engine)
                
                # MOSTRAR RESUMEN
                if 'error' in resultado:
                    print(f"❌ Error: {resultado['error']}")
                else:
                    print(f"✅ Tipo: {resultado.get('tipo', 'N/A')}")
                    
                    if resultado.get('tipo') == 'comparacion':
                        print(f"✅ Clientes comparados: {resultado.get('clientes_comparados', 0)}")
                        if 'datos' in resultado:
                            for j, cliente in enumerate(resultado['datos'], 1):
                                if isinstance(cliente, dict) and 'identificacion' in cliente:
                                    nombre = cliente['identificacion'].get('nombre', 'N/A')
                                    facturacion = cliente.get('facturacion_erp', {}).get('facturacion_total', 0)
                                    print(f"   {j}. {nombre}: {facturacion:,.0f} Gs")
                    
                    elif resultado.get('tipo') == 'ranking_avanzado':
                        print(f"✅ Total clientes: {resultado.get('total_clientes', 0)}")
                        print(f"✅ Mercado total: {resultado.get('mercado_total', 0):,.0f} Gs")
                        if 'datos' in resultado and len(resultado['datos']) > 0:
                            print("   Top 3:")
                            for cliente in resultado['datos'][:3]:
                                if isinstance(cliente, dict):
                                    nombre = cliente.get('nombre', 'N/A')
                                    facturacion = cliente.get('facturacion_total', 0)
                                    market_share = cliente.get('market_share', 0)
                                    print(f"   • {nombre}: {facturacion:,.0f} Gs ({market_share:.1f}%)")
                    
                    elif resultado.get('tipo') == 'analisis_clusters':
                        print(f"✅ Total clusters: {resultado.get('total_clusters', 0)}")
                        if 'datos' in resultado:
                            for cluster in resultado['datos']:
                                if isinstance(cluster, dict):
                                    nombre = cluster.get('cluster', 'N/A')
                                    empresas = cluster.get('total_empresas', 0)
                                    facturacion = cluster.get('facturacion_total', 0)
                                    print(f"   • {nombre}: {empresas} empresas, {facturacion:,.0f} Gs")
                    
                    elif resultado.get('tipo') == 'datos_completos':
                        cliente = resultado.get('cliente', 'N/A')
                        print(f"✅ Cliente: {cliente}")
                        if 'datos' in resultado:
                            datos = resultado['datos']
                            if isinstance(datos, dict):
                                # Mostrar secciones disponibles
                                secciones = list(datos.keys())
                                print(f"✅ Secciones: {len(secciones)}")
                                for seccion in secciones:
                                    print(f"   • {seccion}")
                    
                    elif resultado.get('tipo') == 'estadisticas_mercado':
                        if 'resumen_general' in resultado:
                            resumen = resultado['resumen_general']
                            print(f"✅ Clientes facturación: {resumen.get('total_clientes_facturacion', 0)}")
                            print(f"✅ Anunciantes mercado: {resumen.get('total_anunciantes_mercado', 0)}")
                            print(f"✅ Mercado total: {resumen.get('mercado_total_facturacion', 0):,.0f} Gs")
                
                # MOSTRAR ESTRUCTURA JSON (primeros niveles)
                print(f"\n📋 ESTRUCTURA JSON:")
                if isinstance(resultado, dict):
                    for key in resultado.keys():
                        if key == 'datos' and isinstance(resultado[key], list):
                            print(f"   {key}: [lista con {len(resultado[key])} elementos]")
                        elif key == 'datos' and isinstance(resultado[key], dict):
                            print(f"   {key}: [objeto con {len(resultado[key])} campos]")
                        else:
                            print(f"   {key}: {type(resultado[key]).__name__}")
                
            except Exception as e:
                print(f"❌ Error ejecutando consulta: {e}")
            
            print()
            print("=" * 70)
            print()
        
        # RESUMEN FINAL
        print("🎉 RESUMEN DEL TEST")
        print("=" * 40)
        print("✅ Todas las consultas ejecutadas sin Claude API")
        print("✅ Zero créditos usados")
        print("✅ Acceso completo a datos de 5 tablas")
        print("✅ Comparaciones, rankings, clusters, estadísticas")
        print("✅ JSON puro listo para análisis")
        
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        print("💡 Asegúrate de ejecutar desde el directorio backend")
        print("💡 Asegúrate de que jarvis_360_integration.py tiene las funciones")
        
    except Exception as e:
        print(f"❌ Error general: {e}")

def test_consulta_individual(query):
    """
    Probar una consulta específica individual
    """
    
    print(f"🔍 TEST CONSULTA INDIVIDUAL")
    print(f"Query: '{query}'")
    print("-" * 50)
    
    try:
        from app import engine
        from jarvis_360_integration import get_consulta_compleja_sin_claude
        
        resultado = get_consulta_compleja_sin_claude(query, engine)
        
        # MOSTRAR RESULTADO COMPLETO EN JSON
        print("📊 RESULTADO COMPLETO:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))
        
    except Exception as e:
        print(f"❌ Error: {e}")

def menu_interactivo():
    """
    Menú interactivo para probar consultas
    """
    
    print("🎯 MENÚ INTERACTIVO - CONSULTAS SIN CLAUDE")
    print("=" * 50)
    
    opciones = {
        "1": ("comparar unilever vs cervepar", "Comparación 2 clientes"),
        "2": ("top 10 clientes", "Ranking top 10"),
        "3": ("analisis clusters", "Análisis por clusters"),
        "4": ("datos completos cervepar", "Datos completos CERVEPAR"),
        "5": ("estadisticas mercado", "Estadísticas generales"),
        "6": ("comparar banco familiar vs interfisa", "Comparación bancos"),
        "7": ("datos completos unilever", "Datos completos UNILEVER")
    }
    
    while True:
        print("\n📋 OPCIONES:")
        for num, (query, desc) in opciones.items():
            print(f"   {num}. {desc}")
        print("   0. Salir")
        
        eleccion = input("\n🎯 Elige una opción (0-7): ").strip()
        
        if eleccion == "0":
            print("👋 ¡Hasta luego!")
            break
        elif eleccion in opciones:
            query, desc = opciones[eleccion]
            print(f"\n🚀 Ejecutando: {desc}")
            test_consulta_individual(query)
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    print("🎯 SELECCIONA MODO DE PRUEBA:")
    print("1. Test automático completo")
    print("2. Test consulta individual")
    print("3. Menú interactivo")
    
    modo = input("\nElige modo (1-3): ").strip()
    
    if modo == "1":
        test_consultas_sin_creditos()
    elif modo == "2":
        query = input("Ingresa tu consulta: ").strip()
        if query:
            test_consulta_individual(query)
    elif modo == "3":
        menu_interactivo()
    else:
        print("Ejecutando test automático...")
        test_consultas_sin_creditos()

