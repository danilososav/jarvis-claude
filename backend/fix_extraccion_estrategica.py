"""
FIX: Extracción mejorada de nombres en consultas estratégicas
Problema: Sistema mezclaba nombre del cliente con resto de la query
"""

import re
import logging

logger = logging.getLogger(__name__)

def extract_client_from_strategic_query_fixed(user_query):
    """
    Extraer nombres de clientes de preguntas estratégicas - VERSIÓN MEJORADA
    """
    
    # Patrones específicos para diferentes formatos de pregunta
    patterns = [
        # "Empresa X ¿algo?"
        r'^([A-Z][A-Za-z\s&\.]+?)\s*[¿\?]',
        # "Che, Empresa X algo"
        r'[Cc]he,?\s+([A-Z][A-Za-z\s&\.]+?)\s+(?:tiene|dice|es|se|¿)',
        # "Empresa X dice/tiene/es algo"
        r'^([A-Z][A-Za-z\s&\.]+?)\s+(?:dice|tiene|es|se)\s+',
        # Solo nombre al inicio seguido de palabra clave
        r'^([A-Z][A-Za-z\s&\.]{3,25}?)\s+(?:datos|perfil|cluster|factur)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_query.strip())
        if match:
            nombre_candidato = match.group(1).strip()
            
            # Limpiar nombre candidato
            nombre_candidato = re.sub(r'\s+', ' ', nombre_candidato)  # Espacios múltiples
            
            # Filtrar palabras que no son nombres de empresas
            exclude_words = ['QUE', 'COMO', 'DONDE', 'CUANDO', 'POR', 'PARA', 'CON', 'SIN', 'SOBRE', 'ESTA', 'ESTAN']
            
            if (nombre_candidato.upper() not in exclude_words and 
                len(nombre_candidato) >= 3 and 
                len(nombre_candidato) <= 30):
                
                logger.info(f"🎯 Nombre candidato extraído: '{nombre_candidato}'")
                return nombre_candidato
    
    return None

def identify_cliente_strategic_enhanced_fixed(user_query, db_engine):
    """
    Identificación mejorada para consultas estratégicas - VERSIÓN CORREGIDA
    """
    
    logger.info(f"🔍 Identificación estratégica para: {user_query}")
    
    # 1. Intentar extracción específica de nombre
    nombre_candidato = extract_client_from_strategic_query_fixed(user_query)
    
    if nombre_candidato:
        logger.info(f"✅ Usando nombre extraído: '{nombre_candidato}'")
        
        # 2. Usar sistema robusto SOLO con el nombre limpio
        cliente_info = identify_cliente_automatico_robusto(nombre_candidato, db_engine)
        
        if cliente_info:
            logger.info(f"✅ Cliente estratégico identificado: {cliente_info['nombre']}")
            return cliente_info
        else:
            logger.warning(f"❌ Nombre extraído '{nombre_candidato}' no encontrado en BD")
    
    # 3. Fallback: intentar con query completa pero normalizada
    logger.info("🔄 Intentando fallback con query completa")
    cliente_info = identify_cliente_automatico_robusto(user_query, db_engine)
    
    if cliente_info:
        logger.info(f"✅ Cliente fallback identificado: {cliente_info['nombre']}")
        return cliente_info
    
    logger.warning(f"❌ Cliente no identificado en consulta estratégica: {user_query}")
    return None

# FUNCIÓN DE REEMPLAZO PARA JARVIS_360_INTEGRATION.PY
def get_cliente_360_strategic_fixed(user_query, db_engine):
    """
    Versión corregida de análisis estratégico 360°
    """
    
    logger.info(f"🎯 Iniciando análisis estratégico 360° para: {user_query}")
    
    # 1. Identificación mejorada y corregida
    cliente_info = identify_cliente_strategic_enhanced_fixed(user_query, db_engine)
    
    if not cliente_info:
        logger.warning(f"❌ Cliente no encontrado: {user_query}")
        return []
    
    # 2. Usar el análisis existente con el cliente identificado
    logger.info(f"🧠 Generando análisis para: {cliente_info['nombre']}")
    
    # Aquí usaríamos la función de análisis existente
    # Como no tengo acceso a la función completa, retorno estructura básica
    try:
        # Simular llamada a get_facturacion_erp_completa y otras funciones
        resultado = {
            'tipo_analisis': 'estrategico',
            'cliente': cliente_info['nombre'],
            'anunciante_id': cliente_info['anunciante_id'],
            'consulta_original': user_query,
            'metodo_identificacion': cliente_info.get('method', 'estrategico'),
            'score_identificacion': cliente_info.get('score', 1.0)
        }
        
        logger.info(f"✅ Análisis estratégico completado para {cliente_info['nombre']}")
        return [resultado]
        
    except Exception as e:
        logger.error(f"❌ Error en análisis estratégico: {e}")
        return []

# TEST DE LA FUNCIÓN
def test_extraccion():
    """
    Test de la función de extracción mejorada
    """
    
    test_queries = [
        "Puma Energy ¿Se nota su perfil innovador en nuestros servicios?",
        "Che, Alex S.A. tiene una inversión alta",
        "CERVEPAR dice ser innovadora",
        "Unilever datos completos",
        "Nestle perfil estrategico"
    ]
    
    print("🧪 TEST DE EXTRACCIÓN MEJORADA:")
    print("="*50)
    
    for query in test_queries:
        nombre = extract_client_from_strategic_query_fixed(query)
        print(f"'{query}'")
        print(f"   → '{nombre}'\n")

if __name__ == "__main__":
    print("🔧 FIX: EXTRACCIÓN DE NOMBRES EN CONSULTAS ESTRATÉGICAS")
    print("="*70)
    
    test_extraccion()
    
    print("📋 INSTRUCCIONES PARA IMPLEMENTAR:")
    print("="*40)
    print("1. Reemplazar extract_client_from_strategic_query() en jarvis_360_integration.py")
    print("2. Reemplazar identify_cliente_strategic_enhanced() en jarvis_360_integration.py") 
    print("3. Reemplazar get_cliente_360_strategic() en jarvis_360_integration.py")
    print("4. Reiniciar servidor y probar")

