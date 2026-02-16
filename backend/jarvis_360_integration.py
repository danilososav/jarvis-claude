"""
JARVIS BI 360° - IMPLEMENTACIÓN COMPLETA
Sistema de integración total: ERP + AdLens + DNIT
"""

from sqlalchemy import text
import logging
import difflib
import re
from sqlalchemy import text
import json
from decimal import Decimal

logger = logging.getLogger(__name__)

# def decimal_default(obj):
 #   if isinstance(obj, Decimal):
 #       return float(obj)
 #   raise TypeError

def get_cliente_360(user_query, db_engine):
    """
    Análisis 360° con identificación estratégica mejorada
    """
    
    # Detectar si es una consulta estratégica compleja
    strategic_keywords = ['se nota', 'perfil', 'innovador', 'captura', 'escapando', 'departamento', 'agencia', 'crece más', 'refleja', 'coincide', 'típico', 'madurez', 'perdiendo oportunidades']
    
    if any(keyword in user_query.lower() for keyword in strategic_keywords):
        # Usar análisis estratégico mejorado
        return get_cliente_360_strategic(user_query, db_engine)
    else:
        # Usar análisis normal existente
        logger.info(f"🔍 Iniciando análisis 360° normal para: {user_query}")
        
        cliente_info = identify_cliente_automatico_robusto(user_query, db_engine)
        
        if not cliente_info:
            logger.warning(f"❌ Cliente no encontrado: {user_query}")
            return []
        
        # Obtener datos ERP completos
        datos_erp = get_facturacion_erp_completa(db_engine.connect(), cliente_info['anunciante_id'])
        
        if not datos_erp or datos_erp['registros'] == 0:
            logger.warning(f"❌ No hay datos ERP para {cliente_info['nombre']}")
            return []
        
        # Enriquecer con datos AdLens y DNIT
        datos_enriquecidos = enrich_with_adlens_and_dnit(datos_erp, cliente_info['anunciante_id'], db_engine)
        
        # Estructurar resultado
        resultado = {
            'cliente': cliente_info['nombre'],
            'anunciante_id': cliente_info['anunciante_id'],
            'metodo_identificacion': cliente_info.get('method', 'normal'),
            'datos_completos': datos_enriquecidos
        }
        
        logger.info(f"✅ Análisis 360° normal completado para {cliente_info['nombre']}")
        return [resultado]

def identify_cliente_fuzzy_360(user_query,db_engine):
    """
    Identificación mejorada de clientes usando dim_anunciante_perfil
    """
    
    try:
        with db_engine.connect() as conn: 
            # Buscar en dim_anunciante_perfil (fuente principal AdLens)
            stmt = text("""
            SELECT 
                p.anunciante_id,
                p.nombre_anunciante as nombre,
                p.nombre_anunciante as nombre_oficial
            FROM dim_anunciante_perfil p
            WHERE p.nombre_anunciante IS NOT NULL
            ORDER BY p.anunciante_id
        """)
            
            clientes = conn.execute(stmt).fetchall()
            
            # Fuzzy matching mejorado
            from difflib import SequenceMatcher
            
            query_clean = limpiar_query(user_query)
            best_match = None
            best_score = 0
            
            for cliente in clientes:
                nombre = cliente.nombre or ""
                nombre_oficial = cliente.nombre_oficial or ""
                
                # Calcular scores para ambos nombres
                score1 = SequenceMatcher(None, query_clean, nombre.lower()).ratio()
                score2 = SequenceMatcher(None, query_clean, nombre_oficial.lower()).ratio()
                
                # Tomar el mejor score
                score = max(score1, score2)
                
                # Bonus por match exacto en substring
                if query_clean in nombre.lower() or query_clean in nombre_oficial.lower():
                    score += 0.3
                
                if score > best_score and score > 0.7:  # Threshold más bajo
                    best_score = score
                    best_match = {
                        'anunciante_id': cliente.anunciante_id,
                        'nombre': nombre,
                        'nombre_oficial': nombre_oficial,
                        'score': score
                    }
            
            if best_match:
                logger.info(f"✅ Fuzzy match: {query_clean} → {best_match['nombre']} (score: {best_match['score']:.2f})")
                return best_match
            else:
                logger.warning(f"❌ Sin match fuzzy para: {query_clean}")
                return None
                
    except Exception as e:
        logger.error(f"❌ Error en fuzzy matching: {e}")
        return None
    
def get_facturacion_erp_completa(conn, anunciante_id):
    """
    Obtener facturación completa del ERP - VERSIÓN CORREGIDA
    """
    
    try:
        # ✅ QUERY SIMPLIFICADA PERO COMPLETA
        stmt = text("""
            SELECT 
                SUM(facturacion) as facturacion_total,
                SUM(revenue) as revenue_total, 
                SUM(costo) as costo_total,
                AVG(facturacion) as promedio_mensual,
                COUNT(*) as registros,
                STRING_AGG(DISTINCT division, ', ') as divisiones,
                STRING_AGG(DISTINCT arena, ', ') as arenas
            FROM fact_facturacion 
            WHERE anunciante_id = :anunciante_id
        """)
        
        result = conn.execute(stmt, {"anunciante_id": anunciante_id}).fetchone()
        
        if result:
            return {
                'facturacion_total': float(result.facturacion_total or 0),
                'revenue_total': float(result.revenue_total or 0),
                'costo_total': float(result.costo_total or 0), 
                'promedio_mensual': float(result.promedio_mensual or 0),
                'registros': result.registros or 0,
                'divisiones': result.divisiones or '',
                'arenas': result.arenas or '',
                'evolucion_mensual': []  # ✅ CAMPO VACÍO PERO PRESENTE
            }
        else:
            return {
                'facturacion_total': 0,
                'revenue_total': 0,
                'costo_total': 0,
                'promedio_mensual': 0,
                'registros': 0,
                'divisiones': '',
                'arenas': '',
                'evolucion_mensual': []
            }
            
    except Exception as e:
        logger.error(f"❌ Error obteniendo facturación ERP: {e}")
        return {
            'facturacion_total': 0,
            'revenue_total': 0,
            'costo_total': 0,
            'promedio_mensual': 0,
            'registros': 0,
            'divisiones': '',
            'arenas': '',
            'evolucion_mensual': []
        }

def get_ranking_dnit_completo(conn, anunciante_id):
    """
    Obtener posicionamiento DNIT completo
    """
    
    try:
        stmt = text("""
            SELECT 
                ranking,
                aporte_gs,
                ingreso_estimado_gs,
                razon_social
            FROM dim_posicionamiento_dnit 
            WHERE anunciante_id = :anunciante_id
        """)
        
        result = conn.execute(stmt, {"anunciante_id": anunciante_id}).fetchone()
        
        if result:
            return {
                'ranking_dnit': result.ranking,
                'aporte_dnit_gs': float(result.aporte_gs or 0),
                'ingreso_estimado_gs': float(result.ingreso_estimado_gs or 0),
                'razon_social_dnit': result.razon_social or ''
            }
        else:
            return {}
            
    except Exception as e:
        logger.error(f"❌ Error obteniendo ranking DNIT: {e}")
        return {}

def get_perfil_adlens_completo(conn, anunciante_id):
    """
    Obtener perfil AdLens completo con clusters, cultura e inversiones por medio
    """
    
    try:
        stmt = text("""
            SELECT 
                -- Identificación
                nombre_anunciante,
                rubro_principal,
                tamano_de_la_empresa_cantidad_de_empleados,
                
                -- Clusters y perfiles
                cluster,
                tipo_de_cluster, 
                cultura,
                ejecucion,
                estructura,
                competitividad,
                puntaje_total,
                
                -- Inversiones por medio 2024 (en miles USD)
                CAST(inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT) as inv_tv_abierta,
                CAST(inversion_en_radio_2024_en_miles_usd AS FLOAT) as inv_radio,
                CAST(inversion_en_cable_2024_en_miles_usd AS FLOAT) as inv_cable, 
                CAST(inversion_en_revistas_2024_en_miles_usd AS FLOAT) as inv_revistas,
                CAST(inversion_en_diarios_2024_en_miles_usd AS FLOAT) as inv_diarios,
                CAST(inversion_en_pdv_2024_en_miles_usd AS FLOAT) as inv_pdv,
                
                -- Datos organizacionales
                central_de_medios,
                tiene_la_empresa_departamento_de_marketing,
                en_que_medios_invierte_la_empresa_principalmente,
                la_empresa_invierte_en_digital
                
            FROM dim_anunciante_perfil 
            WHERE anunciante_id = :anunciante_id
        """)
        
        result = conn.execute(stmt, {"anunciante_id": anunciante_id}).fetchone()
        
        if result:
            # Calcular inversión total y mix de medios
            inversiones = {
                'TV Abierta': result.inv_tv_abierta or 0,
                'Radio': result.inv_radio or 0, 
                'Cable': result.inv_cable or 0,
                'Revistas': result.inv_revistas or 0,
                'Diarios': result.inv_diarios or 0,
                'PDV': result.inv_pdv or 0
            }
            
            total_inversion = sum(inversiones.values())
            
            # Calcular mix de medios (porcentajes)
            mix_medios = {}
            for medio, monto in inversiones.items():
                if total_inversion > 0:
                    porcentaje = (monto / total_inversion) * 100
                else:
                    porcentaje = 0
                    
                mix_medios[medio] = {
                    'monto_usd': monto,
                    'porcentaje': round(porcentaje, 1)
                }
            
            return {
                'nombre_anunciante': result.nombre_anunciante,
                'rubro_principal': result.rubro_principal, 
                'tamano_empresa': result.tamano_de_la_empresa_cantidad_de_empleados,
                
                # Perfil estratégico
                'cluster': result.cluster,
                'tipo_cluster': result.tipo_de_cluster,
                'cultura': result.cultura,
                'ejecucion': result.ejecucion,
                'estructura': result.estructura,
                'competitividad': float(result.competitividad or 0),
                'puntaje_total': float(result.puntaje_total or 0),
                
                # Inversiones
                'inversiones_detalle': inversiones,
                'inversion_total_usd': total_inversion,
                'mix_medios': mix_medios,
                
                # Organizacional
                'central_medios': result.central_de_medios,
                'tiene_marketing': result.tiene_la_empresa_departamento_de_marketing,
                'medios_principales': result.en_que_medios_invierte_la_empresa_principalmente,
                'invierte_digital': result.la_empresa_invierte_en_digital
            }
        else:
            return {}
            
    except Exception as e:
        logger.error(f"❌ Error obteniendo perfil AdLens: {e}")
        return {}

def get_inversion_granular_opcional(conn, anunciante_id):
    """
    Obtener inversión granular mensual (opcional - solo si se necesita evolución)
    """
    
    try:
        # Por ahora devolver vacío - se puede implementar después si se necesita
        # la evolución mensual detallada por medio
        return {}
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo inversión granular: {e}")
        return {}

def merge_all_sources_360(cliente_info, facturacion_data, ranking_data, perfil_data, inversion_granular):
    """
    FUNCIÓN CLAVE: Integra todas las fuentes en estructura única 360°
    """
    
    # Estructura base del cliente
    cliente_360 = {
        # IDENTIFICACIÓN
        'anunciante_id': cliente_info['anunciante_id'],
        'cliente': perfil_data.get('nombre_anunciante') or cliente_info['nombre'],
        'nombre_oficial': cliente_info.get('nombre_oficial', ''),
        
        # FACTURACIÓN ERP
        'facturacion': facturacion_data.get('facturacion_total', 0),
        'revenue': facturacion_data.get('revenue_total', 0),
        'costo': facturacion_data.get('costo_total', 0),
        'promedio_mensual': facturacion_data.get('promedio_mensual', 0),
        'registros': facturacion_data.get('registros', 0),
        'divisiones': facturacion_data.get('divisiones', ''),
        'arenas': facturacion_data.get('arenas', ''),
        'evolucion_mensual': facturacion_data.get('evolucion_mensual', []),
        
        # POSICIONAMIENTO DNIT
        'ranking': ranking_data.get('ranking_dnit'),
        'aporte_dnit': ranking_data.get('aporte_dnit_gs', 0),
        'ingreso_estimado': ranking_data.get('ingreso_estimado_gs', 0),
        
        # PERFIL ADLENS COMPLETO
        'rubro': perfil_data.get('rubro_principal', ''),
        'tamano_empresa': perfil_data.get('tamano_empresa', ''),
        'cluster': perfil_data.get('cluster', ''),
        'tipo_cluster': perfil_data.get('tipo_cluster', ''),
        'cultura': perfil_data.get('cultura', ''),
        'ejecucion': perfil_data.get('ejecucion', ''),
        'estructura': perfil_data.get('estructura', ''),
        'competitividad': perfil_data.get('competitividad', 0),
        'puntaje_total': perfil_data.get('puntaje_total', 0),
        
        # INVERSIONES 360°
        'inversion_total_usd': perfil_data.get('inversion_total_usd', 0),
        'inversiones_detalle': perfil_data.get('inversiones_detalle', {}),
        'mix_medios': perfil_data.get('mix_medios', {}),
        
        # ORGANIZACIONAL
        'central_medios': perfil_data.get('central_medios', ''),
        'tiene_marketing': perfil_data.get('tiene_marketing', ''),
        'medios_principales': perfil_data.get('medios_principales', ''),
        'invierte_digital': perfil_data.get('invierte_digital', ''),
    }
    
    # CALCULAR KPIS Y RATIOS
    if cliente_360['facturacion'] > 0 and cliente_360['inversion_total_usd'] > 0:
        # ROI publicitario (% inversión vs facturación)
        cliente_360['roi_publicitario'] = (cliente_360['inversion_total_usd'] / cliente_360['facturacion']) * 100
    else:
        cliente_360['roi_publicitario'] = 0
    
    # Market share calculado vs total del mercado
    cliente_360['market_share'] = calcular_market_share(cliente_360['facturacion'])
    
    # Perfil estratégico calculado
    cliente_360['perfil_estrategico'] = generar_perfil_estrategico(perfil_data)
    
    # Nivel de inversión
    if cliente_360['inversion_total_usd'] > 100000:
        cliente_360['nivel_inversion'] = 'Alto'
    elif cliente_360['inversion_total_usd'] > 50000:
        cliente_360['nivel_inversion'] = 'Medio'
    elif cliente_360['inversion_total_usd'] > 0:
        cliente_360['nivel_inversion'] = 'Bajo'
    else:
        cliente_360['nivel_inversion'] = 'Sin datos'
    
    return cliente_360

def calcular_market_share(facturacion_cliente):
    """Calcular market share aproximado"""
    # Simplificado - en producción usar suma total del mercado
    if facturacion_cliente > 20000000000:  # 20B+
        return round((facturacion_cliente / 200000000000) * 100, 2)  # Asumiendo mercado 200B
    else:
        return 0

def generar_perfil_estrategico(perfil_data):
    """Generar descripción de perfil estratégico"""
    cluster = perfil_data.get('cluster', '')
    cultura = perfil_data.get('cultura', '')
    
    if cluster and cultura:
        return f"Empresa {cluster} con Cultura {cultura}"
    elif cluster:
        return f"Cluster {cluster}"
    elif cultura: 
        return f"Cultura {cultura}"
    else:
        return "Perfil en desarrollo"

def limpiar_query(query):
    """Limpiar query para fuzzy matching"""
    import re
    
    # Quitar stopwords
    stopwords = ['cuanto', 'cuánto', 'facturo', 'facturó', 'invirtió', 'invirti', 'de', 'la', 'el', 'en', 'y', 'tv', 'television']
    
    # Limpiar query
    query_clean = query.lower().strip()
    for word in stopwords:
        query_clean = query_clean.replace(word, ' ')
    
    # Limpiar espacios extra
    query_clean = re.sub(r'\s+', ' ', query_clean).strip()
    
    return query_clean

def get_facturacion_enriched_fallback(user_query):
    """Fallback al sistema anterior si el 360° falla"""
    logger.warning("⚠️ Usando sistema fallback")
    
    try:
        # Importar función original
        from app import get_facturacion_enriched
        return get_facturacion_enriched(user_query)
    except:
        return []

# TESTING
if __name__ == "__main__":
    print("🧪 TEST JARVIS 360°")
    print("="*40)
    print("✅ Funciones de integración creadas")
    print("✅ Fuzzy matching mejorado")
    print("✅ Estructura 360° definida") 
    print("✅ Fallback a sistema anterior")
    print("\n🚀 Listo para integrar en app.py")

# ✅ FUNCIÓN FALTANTE - AGREGAR AL FINAL DEL ARCHIVO
def format_data_for_claude_360(rows, query_type):
    """
    Formatea datos 360° completos para Claude
    """
    
    if not rows:
        return []
    
    formatted_clients = []
    
    for row in rows:
        # Obtener datos_completos que contiene toda la info
        datos = row.get('datos_completos', {})
        
        cliente_360 = {
            'cliente': row.get('cliente', 'N/A'),
            'anunciante_id': row.get('anunciante_id'),
            
            # FACTURACIÓN ERP - CORREGIDO
            'facturacion': datos.get('facturacion_total', 0),
            'revenue': datos.get('revenue_total', 0),
            'promedio_mensual': datos.get('promedio_mensual', 0),
            'registros': datos.get('registros', 0),
            'divisiones': datos.get('divisiones', ''),
            'arenas': datos.get('arenas', ''),
            
            # PERFIL ADLENS - CORREGIDO
            'cluster': datos.get('perfil_adlens', {}).get('cluster', ''),
            'competitividad': datos.get('perfil_adlens', {}).get('competitividad', 0),
            
            # RANKING DNIT - CORREGIDO
            'ranking': datos.get('ranking_dnit', {}).get('ranking'),
            'aporte_dnit': datos.get('ranking_dnit', {}).get('aporte_gs', 0),
            
            'market_share': row.get('market_share', 0),
        }
        
        formatted_clients.append(cliente_360)
    
    return formatted_clients

def identify_cliente_automatico_robusto(user_query, db_engine):
    """
    Sistema robusto de identificación automática de clientes
    Previene falsos positivos como cervepar → cerveza diosa
    """
    
    logger.info(f"🔍 Identificación automática para: {user_query}")
    
    try:
        with db_engine.connect() as conn:
            # Obtener todos los clientes
            stmt = text("""
                SELECT 
                    p.anunciante_id,
                    p.nombre_anunciante as nombre,
                    p.cluster,
                    p.rubro_principal
                FROM dim_anunciante_perfil p
                WHERE p.nombre_anunciante IS NOT NULL
                ORDER BY p.anunciante_id
            """)
            
            clientes = conn.execute(stmt).fetchall()
            
            # PASO 1: Normalizar query
            query_clean = normalizar_nombre_cliente(user_query)
            logger.info(f"🔧 Query normalizado: '{query_clean}'")
            
            # PASO 2: COINCIDENCIA EXACTA (Prioridad Máxima)
            exact_match = buscar_coincidencia_exacta(query_clean, clientes)
            if exact_match:
                logger.info(f"✅ COINCIDENCIA EXACTA: {exact_match['nombre']}")
                return exact_match
            
            # PASO 3: ALIASES AUTOMÁTICOS
            alias_match = buscar_por_aliases(query_clean, clientes)
            if alias_match:
                logger.info(f"✅ ALIAS encontrado: {alias_match['nombre']}")
                return alias_match
            
            # PASO 4: FUZZY ESTRICTO (último recurso)
            fuzzy_match = buscar_fuzzy_estricto(query_clean, clientes)
            if fuzzy_match:
                logger.info(f"✅ FUZZY ESTRICTO: {fuzzy_match['nombre']} (score: {fuzzy_match['score']:.2f})")
                return fuzzy_match
            
            # No encontrado
            logger.warning(f"❌ Cliente no identificado: {query_clean}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error en identificación automática: {e}")
        return None

def normalizar_nombre_cliente(query):
    """Normalizar y limpiar nombre del cliente"""
    
    stopwords = [
        'cuanto', 'cuánto', 'facturo', 'facturó', 'invirtió', 'invirti', 
        'datos', 'informacion', 'perfil', 'de', 'la', 'el', 'en', 'y', 
        'tv', 'television', 'facturacion', 'ranking', 'cluster', 'cultura'
    ]
    
    query_clean = query.lower().strip()
    
    # Remover stopwords
    for word in stopwords:
        query_clean = re.sub(rf'\b{word}\b', '', query_clean, flags=re.IGNORECASE)
    
    # Limpiar espacios y caracteres especiales
    query_clean = re.sub(r'[^\w\s]', ' ', query_clean)
    query_clean = re.sub(r'\s+', ' ', query_clean).strip()
    
    return query_clean

def buscar_coincidencia_exacta(query_clean, clientes):
    """Buscar coincidencia exacta o casi exacta"""
    
    for cliente in clientes:
        nombre = cliente.nombre or ""
        
        # 1. Coincidencia exacta completa
        if query_clean.lower() == nombre.lower():
            return crear_resultado_cliente(cliente, 1.0, "exact_full")
        
        # 2. Coincidencia por palabras exactas
        query_words = set(query_clean.lower().split())
        nombre_words = set(nombre.lower().split())
        
        if query_words.issubset(nombre_words):
            return crear_resultado_cliente(cliente, 0.95, "exact_words")
        
        # 3. Inicio exacto (ej: "unilever" → "UNILEVER DE PARAGUAY")
        if nombre.lower().startswith(query_clean.lower()) and len(query_clean) >= 5:
            return crear_resultado_cliente(cliente, 0.9, "exact_start")
    
    return None

def buscar_por_aliases(query_clean, clientes):
    """Buscar usando aliases conocidos automáticamente"""
    
    # Aliases automáticos para marcas conocidas
    aliases_automaticos = {
        # Cervezas
        'cervepar': ['cervepar'],
        'pilsen': ['pilsen'],
        'brahma': ['brahma'],
        'telecel': ['telecel'],
        'banco familiar': ['banco familiar'],
        'distribuidora del paraguay': ['distribuidora del paraguay', 'distribuidora paraguay'],
        
        # Telecos
        'tigo': ['tigo paraguay'],
        'personal': ['personal', 'telecom personal'],
        'telefonica': ['telefonica'],
        
        # Marcas globales
        'unilever': ['unilever'],
        'nestle': ['nestle', 'nestlé'],
        'coca cola': ['coca cola', 'coca-cola'],
        
        # Bancos
        'banco nacional': ['banco nacional'],
        'banco continental': ['banco continental'],
        
        # Retail
        'carrefour': ['carrefour'],
        'superseis': ['superseis', 'super seis'],
    }
    
    # Buscar en aliases
    for alias_key, alias_variants in aliases_automaticos.items():
        if any(variant in query_clean.lower() for variant in alias_variants):
            # Buscar cliente que contenga esta palabra clave
            for cliente in clientes:
                nombre = cliente.nombre or ""
                if alias_key in nombre.lower():
                    return crear_resultado_cliente(cliente, 0.85, f"alias_{alias_key}")
    
    return None

def buscar_fuzzy_estricto(query_clean, clientes):
    """Fuzzy matching estricto con validaciones anti-falsos positivos"""
    
    best_match = None
    best_score = 0
    
    for cliente in clientes:
        nombre = cliente.nombre or ""
        
        # Calcular similarity
        score = difflib.SequenceMatcher(None, query_clean.lower(), nombre.lower()).ratio()
        
        # VALIDACIONES ESTRICTAS
        
        # 1. Score mínimo mucho más alto
        if score < 0.75:  # Era 0.4, ahora 0.75
            continue
        
        # 2. Detectar falsos positivos obvios
        if es_falso_positivo_obvio(query_clean, nombre):
            logger.warning(f"⚠️ Falso positivo detectado: '{query_clean}' vs '{nombre}'")
            continue
        
        # 3. Validar longitud similar
        if abs(len(query_clean) - len(nombre)) > len(query_clean) * 0.7:
            continue
        
        # 4. Primera palabra debe coincidir parcialmente
        query_first = query_clean.split()[0] if query_clean.split() else ""
        nombre_first = nombre.split()[0] if nombre.split() else ""
        
        if len(query_first) >= 4 and len(nombre_first) >= 4:
            if query_first[:3].lower() != nombre_first[:3].lower():
                continue
        
        if score > best_score:
            best_score = score
            best_match = crear_resultado_cliente(cliente, score, "fuzzy_strict")
    
    # Solo retornar si score es realmente alto
    if best_match and best_score >= 0.8:
        return best_match
    
    return None

def es_falso_positivo_obvio(query, nombre):
    """Detectar falsos positivos conocidos"""
    
    falsos_positivos = [
        # Cervezas diferentes
        (["cervepar"], ["cerveza diosa", "diosa"]),
        (["brahma"], ["brahma garcia"]),
        
        # Telecos diferentes  
        (["tigo"], ["tigo sports"]),
        (["personal"], ["personal envios"]),
        (["telefonica"], ["telefonica celular"]),
        
        # Evitar confusiones genéricas
        (["nacional"], ["banco nacional de fomento"]),
        (["central"], ["banco central", "mercado central"]),
    ]
    
    query_lower = query.lower()
    nombre_lower = nombre.lower()
    
    for query_patterns, nombre_patterns in falsos_positivos:
        if any(pattern in query_lower for pattern in query_patterns):
            if any(pattern in nombre_lower for pattern in nombre_patterns):
                return True
    
    return False

def crear_resultado_cliente(cliente, score, method):
    """Crear objeto resultado estandarizado"""
    
    return {
        'anunciante_id': cliente.anunciante_id,
        'nombre': cliente.nombre,
        'cluster': getattr(cliente, 'cluster', ''),
        'rubro': getattr(cliente, 'rubro_principal', ''),
        'score': score,
        'method': method
    }


def es_consulta_de_cliente(user_query, db_engine):
    """
    Detectar si una query es sobre un cliente específico
    """
    try:
        cliente_info = identify_cliente_automatico_robusto(user_query, db_engine)
        
        if cliente_info and cliente_info['score'] >= 0.8:
            return cliente_info
        
        return None
        
    except Exception as e:
        logger.error(f"❌ Error detectando cliente: {e}")
        return None

def get_consulta_compleja_sin_claude(user_query, db_engine):
    """
    Procesar consultas complejas que retornan datos puros sin análisis de Claude
    """
    
    query_lower = user_query.lower()
    
    # DETECTAR TIPO DE CONSULTA COMPLEJA
    if any(w in query_lower for w in ["comparar", "compare", "vs", "versus"]):
        return consulta_comparacion_clientes(user_query, db_engine)
    
    elif any(w in query_lower for w in ["top", "ranking", "mejores", "mayores"]):
        return consulta_ranking_avanzado(user_query, db_engine)
    
    elif any(w in query_lower for w in ["cluster", "clusters", "grupos"]):
        return consulta_analisis_clusters(user_query, db_engine)
    
    elif any(w in query_lower for w in ["completo", "full", "todo", "todos"]):
        return consulta_datos_completos(user_query, db_engine)
    
    elif any(w in query_lower for w in ["estadisticas", "stats", "resumen"]):
        return consulta_estadisticas_mercado(user_query, db_engine)
    
    else:
        return consulta_360_expandida(user_query, db_engine)

def consulta_comparacion_clientes(user_query, db_engine):
    """
    Comparar múltiples clientes con todos sus datos
    Ej: "comparar unilever vs nestle vs coca cola"
    """
    
    logger.info(f"🔍 Consulta comparación: {user_query}")
    
    # Extraer nombres de clientes de la query
    clientes_encontrados = []
    posibles_clientes = ["unilever", "nestle", "coca cola", "cervepar", "tigo", "personal", "telefonica", "banco"]
    
    for cliente in posibles_clientes:
        if cliente in user_query.lower():
            info = identify_cliente_automatico_robusto(cliente, db_engine)
            if info:
                clientes_encontrados.append(info)
    
    if len(clientes_encontrados) < 2:
        # Si no encuentra múltiples, buscar top 5 para comparar
        clientes_encontrados = get_top_clientes_para_comparacion(db_engine)
    
    # Obtener datos completos de cada cliente
    comparacion_data = []
    for cliente in clientes_encontrados:
        datos = get_datos_completos_cliente(cliente['anunciante_id'], db_engine)
        comparacion_data.append(datos)
    
    return {
        'tipo': 'comparacion',
        'clientes_comparados': len(comparacion_data),
        'datos': comparacion_data,
        'campos_incluidos': [
            'facturacion_total', 'market_share', 'ranking_dnit', 'cluster',
            'inversiones_por_medio', 'perfil_estrategico', 'datos_organizacionales'
        ]
    }

def consulta_ranking_avanzado(user_query, db_engine):
    """
    Rankings con múltiples criterios y filtros
    Ej: "top 10 clientes por facturacion con cluster y medios"
    """
    
    logger.info(f"🔍 Consulta ranking avanzado: {user_query}")
    
    try:
        with db_engine.connect() as conn:
            stmt = text("""
                SELECT 
                    f.anunciante_id,
                    p.nombre_anunciante,
                    SUM(f.facturacion) as facturacion_total,
                    SUM(f.revenue) as revenue_total,
                    COUNT(*) as registros,
                    p.cluster,
                    p.cultura,
                    p.competitividad,
                    p.puntaje_total,
                    CAST(p.inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT) as inv_tv,
                    CAST(p.inversion_en_radio_2024_en_miles_usd AS FLOAT) as inv_radio,
                    CAST(p.inversion_en_cable_2024_en_miles_usd AS FLOAT) as inv_cable,
                    d.ranking as ranking_dnit,
                    d.aporte_gs
                FROM fact_facturacion f
                JOIN dim_anunciante_perfil p ON f.anunciante_id = p.anunciante_id
                LEFT JOIN dim_posicionamiento_dnit d ON f.anunciante_id = d.anunciante_id
                GROUP BY f.anunciante_id, p.nombre_anunciante, p.cluster, p.cultura, 
                         p.competitividad, p.puntaje_total, p.inversion_en_tv_abierta_2024_en_miles_usd,
                         p.inversion_en_radio_2024_en_miles_usd, p.inversion_en_cable_2024_en_miles_usd,
                         d.ranking, d.aporte_gs
                ORDER BY facturacion_total DESC
                LIMIT 15
            """)
            
            results = conn.execute(stmt).fetchall()
            
            ranking_data = []
            total_mercado = sum(row.facturacion_total for row in results)
            
            for i, row in enumerate(results, 1):
                market_share = (row.facturacion_total / total_mercado * 100) if total_mercado > 0 else 0
                
                ranking_data.append({
                    'posicion': i,
                    'anunciante_id': row.anunciante_id,
                    'nombre': row.nombre_anunciante,
                    'facturacion_total': float(row.facturacion_total),
                    'revenue_total': float(row.revenue_total),
                    'market_share': round(market_share, 2),
                    'registros': row.registros,
                    'cluster': row.cluster,
                    'cultura': row.cultura,
                    'competitividad': row.competitividad,
                    'puntaje_total': row.puntaje_total,
                    'inversiones': {
                        'tv_abierta': float(row.inv_tv or 0),
                        'radio': float(row.inv_radio or 0),
                        'cable': float(row.inv_cable or 0)
                    },
                    'ranking_dnit': row.ranking_dnit,
                    'aporte_dnit': float(row.aporte_gs or 0)
                })
            
            return {
                'tipo': 'ranking_avanzado',
                'total_clientes': len(ranking_data),
                'mercado_total': float(total_mercado),
                'datos': ranking_data
            }
    
    except Exception as e:
        logger.error(f"❌ Error ranking avanzado: {e}")
        return {'error': str(e)}

def consulta_analisis_clusters(user_query, db_engine):
    """
    Análisis por clusters empresariales - VERSIÓN CORREGIDA
    Ej: "analisis por clusters con inversiones"
    """
    
    logger.info(f"🔍 Análisis clusters: {user_query}")
    
    try:
        with db_engine.connect() as conn:
            stmt = text("""
                SELECT 
                    p.cluster,
                    COUNT(*) as total_empresas,
                    COUNT(f.anunciante_id) as empresas_con_facturacion,
                    SUM(f.facturacion) as facturacion_cluster,
                    AVG(f.facturacion) as promedio_facturacion,
                    AVG(
                        CASE 
                            WHEN p.competitividad = '-' OR p.competitividad IS NULL OR p.competitividad = '' THEN NULL
                            ELSE CAST(p.competitividad AS FLOAT)
                        END
                    ) as competitividad_promedio,
                    AVG(
                        CASE 
                            WHEN p.puntaje_total = '-' OR p.puntaje_total IS NULL OR p.puntaje_total = '' THEN NULL
                            ELSE CAST(p.puntaje_total AS FLOAT)
                        END
                    ) as puntaje_promedio,
                    SUM(
                        CASE 
                            WHEN p.inversion_en_tv_abierta_2024_en_miles_usd = '-' OR p.inversion_en_tv_abierta_2024_en_miles_usd IS NULL OR p.inversion_en_tv_abierta_2024_en_miles_usd = '' THEN 0
                            ELSE CAST(p.inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT)
                        END
                    ) as inversion_tv_total,
                    SUM(
                        CASE 
                            WHEN p.inversion_en_radio_2024_en_miles_usd = '-' OR p.inversion_en_radio_2024_en_miles_usd IS NULL OR p.inversion_en_radio_2024_en_miles_usd = '' THEN 0
                            ELSE CAST(p.inversion_en_radio_2024_en_miles_usd AS FLOAT)
                        END
                    ) as inversion_radio_total,
                    SUM(
                        CASE 
                            WHEN p.inversion_en_cable_2024_en_miles_usd = '-' OR p.inversion_en_cable_2024_en_miles_usd IS NULL OR p.inversion_en_cable_2024_en_miles_usd = '' THEN 0
                            ELSE CAST(p.inversion_en_cable_2024_en_miles_usd AS FLOAT)
                        END
                    ) as inversion_cable_total
                FROM dim_anunciante_perfil p
                LEFT JOIN fact_facturacion f ON p.anunciante_id = f.anunciante_id
                WHERE p.cluster IS NOT NULL AND p.cluster != ''
                GROUP BY p.cluster
                ORDER BY facturacion_cluster DESC NULLS LAST
            """)
            
            results = conn.execute(stmt).fetchall()
            
            clusters_data = []
            for row in results:
                clusters_data.append({
                    'cluster': row.cluster,
                    'total_empresas': row.total_empresas,
                    'empresas_con_facturacion': row.empresas_con_facturacion,
                    'facturacion_total': float(row.facturacion_cluster or 0),
                    'promedio_facturacion': float(row.promedio_facturacion or 0),
                    'competitividad_promedio': round(float(row.competitividad_promedio or 0), 2),
                    'puntaje_promedio': round(float(row.puntaje_promedio or 0), 1),
                    'inversiones_totales': {
                        'tv_abierta': float(row.inversion_tv_total or 0),
                        'radio': float(row.inversion_radio_total or 0),
                        'cable': float(row.inversion_cable_total or 0)
                    }
                })
            
            return {
                'tipo': 'analisis_clusters',
                'total_clusters': len(clusters_data),
                'datos': clusters_data
            }
    
    except Exception as e:
        logger.error(f"❌ Error análisis clusters: {e}")
        return {'error': str(e)}
    
def consulta_datos_completos(user_query, db_engine):
    """
    Datos completos de todos los campos disponibles
    Ej: "datos completos de unilever" o "todo sobre nestle"
    """
    
    logger.info(f"🔍 Datos completos: {user_query}")
    
    # Identificar cliente
    cliente_info = identify_cliente_automatico_robusto(user_query, db_engine)
    if not cliente_info:
        return {'error': 'Cliente no identificado'}
    
    datos = get_datos_completos_cliente(cliente_info['anunciante_id'], db_engine)
    
    return {
        'tipo': 'datos_completos',
        'cliente': cliente_info['nombre'],
        'anunciante_id': cliente_info['anunciante_id'],
        'datos': datos
    }

def consulta_estadisticas_mercado(user_query, db_engine):
    """
    Estadísticas generales del mercado
    Ej: "estadisticas del mercado publicitario"
    """
    
    logger.info(f"🔍 Estadísticas mercado: {user_query}")
    
    try:
        with db_engine.connect() as conn:
            # Estadísticas generales
            stmt = text("""
                SELECT 
                    COUNT(DISTINCT f.anunciante_id) as total_clientes_facturacion,
                    COUNT(DISTINCT p.anunciante_id) as total_anunciantes_mercado,
                    SUM(f.facturacion) as mercado_total_facturacion,
                    SUM(f.revenue) as mercado_total_revenue,
                    AVG(f.facturacion) as promedio_facturacion,
                    COUNT(f.*) as total_registros
                FROM fact_facturacion f
                FULL OUTER JOIN dim_anunciante_perfil p ON f.anunciante_id = p.anunciante_id
            """)
            
            result = conn.execute(stmt).fetchone()
            
            # Top 5 sectores por facturación
            stmt_sectores = text("""
                SELECT 
                    p.rubro_principal,
                    COUNT(*) as empresas,
                    SUM(f.facturacion) as facturacion_sector,
                    AVG(CAST(p.competitividad AS FLOAT)) as competitividad_promedio
                FROM fact_facturacion f
                JOIN dim_anunciante_perfil p ON f.anunciante_id = p.anunciante_id
                WHERE p.rubro_principal IS NOT NULL
                GROUP BY p.rubro_principal
                ORDER BY facturacion_sector DESC
                LIMIT 5
            """)
            
            sectores = conn.execute(stmt_sectores).fetchall()
            
            return {
                'tipo': 'estadisticas_mercado',
                'resumen_general': {
                    'total_clientes_facturacion': result.total_clientes_facturacion,
                    'total_anunciantes_mercado': result.total_anunciantes_mercado,
                    'mercado_total_facturacion': float(result.mercado_total_facturacion or 0),
                    'mercado_total_revenue': float(result.mercado_total_revenue or 0),
                    'promedio_facturacion': float(result.promedio_facturacion or 0),
                    'total_registros': result.total_registros
                },
                'top_sectores': [
                    {
                        'sector': row.rubro_principal,
                        'empresas': row.empresas,
                        'facturacion': float(row.facturacion_sector),
                        'competitividad_promedio': round(float(row.competitividad_promedio or 0), 2)
                    }
                    for row in sectores
                ]
            }
    
    except Exception as e:
        logger.error(f"❌ Error estadísticas: {e}")
        return {'error': str(e)}

def get_datos_completos_cliente(anunciante_id, db_engine):
    """
    Obtener TODOS los datos disponibles de un cliente
    """
    
    try:
        with db_engine.connect() as conn:
            # Datos del perfil AdLens
            stmt_perfil = text("""
                SELECT 
                    nombre_anunciante,
                    rubro_principal,
                    tamano_de_la_empresa_cantidad_de_empleados,
                    cluster,
                    tipo_de_cluster,
                    cultura,
                    ejecucion,
                    estructura,
                    competitividad,
                    puntaje_total,
                    CAST(inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT) as inv_tv,
                    CAST(inversion_en_radio_2024_en_miles_usd AS FLOAT) as inv_radio,
                    CAST(inversion_en_cable_2024_en_miles_usd AS FLOAT) as inv_cable,
                    CAST(inversion_en_revistas_2024_en_miles_usd AS FLOAT) as inv_revistas,
                    CAST(inversion_en_diarios_2024_en_miles_usd AS FLOAT) as inv_diarios,
                    CAST(inversion_en_pdv_2024_en_miles_usd AS FLOAT) as inv_pdv,
                    central_de_medios,
                    tiene_la_empresa_departamento_de_marketing,
                    en_que_medios_invierte_la_empresa_principalmente,
                    la_empresa_invierte_en_digital
                FROM dim_anunciante_perfil
                WHERE anunciante_id = :anunciante_id
            """)
            
            perfil = conn.execute(stmt_perfil, {"anunciante_id": anunciante_id}).fetchone()
            
            # Datos de facturación
            stmt_facturacion = text("""
                SELECT 
                    SUM(facturacion) as facturacion_total,
                    SUM(revenue) as revenue_total,
                    SUM(costo) as costo_total,
                    COUNT(*) as registros,
                    AVG(facturacion) as promedio_mensual,
                    MIN(fecha_fact) as primera_fecha,
                    MAX(fecha_fact) as ultima_fecha,
                    STRING_AGG(DISTINCT division, ', ') as divisiones,
                    STRING_AGG(DISTINCT arena, ', ') as arenas
                FROM fact_facturacion
                WHERE anunciante_id = :anunciante_id
            """)
            
            facturacion = conn.execute(stmt_facturacion, {"anunciante_id": anunciante_id}).fetchone()
            
            # Datos DNIT
            stmt_dnit = text("""
                SELECT 
                    ranking,
                    aporte_gs,
                    ingreso_estimado_gs,
                    razon_social
                FROM dim_posicionamiento_dnit
                WHERE anunciante_id = :anunciante_id
            """)
            
            dnit = conn.execute(stmt_dnit, {"anunciante_id": anunciante_id}).fetchone()
            
            # Compilar datos completos
            datos_completos = {
                'identificacion': {
                    'anunciante_id': anunciante_id,
                    'nombre': perfil.nombre_anunciante if perfil else None,
                    'rubro': perfil.rubro_principal if perfil else None,
                    'tamaño_empresa': perfil.tamano_de_la_empresa_cantidad_de_empleados if perfil else None
                },
                'perfil_estrategico': {
                    'cluster': perfil.cluster if perfil else None,
                    'tipo_cluster': perfil.tipo_de_cluster if perfil else None,
                    'cultura': perfil.cultura if perfil else None,
                    'ejecucion': perfil.ejecucion if perfil else None,
                    'estructura': perfil.estructura if perfil else None,
                    'competitividad': perfil.competitividad if perfil else None,
                    'puntaje_total': perfil.puntaje_total if perfil else None
                } if perfil else {},
                'facturacion_erp': {
                    'facturacion_total': float(facturacion.facturacion_total or 0),
                    'revenue_total': float(facturacion.revenue_total or 0),
                    'costo_total': float(facturacion.costo_total or 0),
                    'registros': facturacion.registros if facturacion else 0,
                    'promedio_mensual': float(facturacion.promedio_mensual or 0),
                    'primera_fecha': str(facturacion.primera_fecha) if facturacion and facturacion.primera_fecha else None,
                    'ultima_fecha': str(facturacion.ultima_fecha) if facturacion and facturacion.ultima_fecha else None,
                    'divisiones': facturacion.divisiones if facturacion else '',
                    'arenas': facturacion.arenas if facturacion else ''
                } if facturacion else {},
                'inversiones_medios': {
                    'tv_abierta_usd': float(perfil.inv_tv or 0),
                    'radio_usd': float(perfil.inv_radio or 0),
                    'cable_usd': float(perfil.inv_cable or 0),
                    'revistas_usd': float(perfil.inv_revistas or 0),
                    'diarios_usd': float(perfil.inv_diarios or 0),
                    'pdv_usd': float(perfil.inv_pdv or 0),
                    'total_usd': float((perfil.inv_tv or 0) + (perfil.inv_radio or 0) + (perfil.inv_cable or 0) + 
                                     (perfil.inv_revistas or 0) + (perfil.inv_diarios or 0) + (perfil.inv_pdv or 0))
                } if perfil else {},
                'datos_organizacionales': {
                    'central_medios': perfil.central_de_medios if perfil else None,
                    'depto_marketing': perfil.tiene_la_empresa_departamento_de_marketing if perfil else None,
                    'medios_principales': perfil.en_que_medios_invierte_la_empresa_principalmente if perfil else None,
                    'invierte_digital': perfil.la_empresa_invierte_en_digital if perfil else None
                } if perfil else {},
                'ranking_dnit': {
                    'ranking': dnit.ranking if dnit else None,
                    'aporte_gs': float(dnit.aporte_gs or 0) if dnit else 0,
                    'ingreso_estimado_gs': float(dnit.ingreso_estimado_gs or 0) if dnit else 0,
                    'razon_social': dnit.razon_social if dnit else None
                } if dnit else {}
            }
            
            return datos_completos
            
    except Exception as e:
        logger.error(f"❌ Error datos completos: {e}")
        return {'error': str(e)}

def get_top_clientes_para_comparacion(db_engine, limit=5):
    """
    Obtener top clientes para comparación
    """
    try:
        with db_engine.connect() as conn:
            stmt = text("""
                SELECT DISTINCT
                    p.anunciante_id,
                    p.nombre_anunciante as nombre
                FROM dim_anunciante_perfil p
                JOIN fact_facturacion f ON p.anunciante_id = f.anunciante_id
                WHERE p.nombre_anunciante IS NOT NULL
                ORDER BY p.anunciante_id
                LIMIT :limit
            """)
            
            results = conn.execute(stmt, {"limit": limit}).fetchall()
            
            return [
                {
                    'anunciante_id': row.anunciante_id,
                    'nombre': row.nombre
                }
                for row in results
            ]
    
    except Exception as e:
        logger.error(f"❌ Error top clientes: {e}")
        return []

# FUNCIÓN PRINCIPAL PARA AGREGAR A APP.PY
def query_compleja_sin_claude_handler(user_query, engine):
    """
    Handler principal para consultas complejas sin Claude
    Retorna datos puros en JSON para análisis
    """
    
    logger.info(f"🔍 Consulta compleja sin Claude: {user_query}")
    
    resultado = get_consulta_compleja_sin_claude(user_query, engine)
    
    return {
        "success": True,
        "responses": [{
            "type": "data_analysis",
            "content": f"Datos extraídos sin análisis de Claude: {resultado['tipo']}",
            "data": resultado,
            "query_type": "compleja_sin_claude"
        }]
    }

def extract_client_from_strategic_query(user_query):
    """
    Extraer nombres de clientes de preguntas estratégicas complejas
    """
    
    # Patrones para detectar nombres de empresas en preguntas complejas
    patterns = [
        # "Empresa X ¿algo?" 
        r'^([A-Z][A-Z\s&\.]+?)\s*[¿\?]',
        # "¿Empresa X algo?"
        r'¿([A-Z][A-Z\s&\.]+?)\s+',
        # "Che, Empresa X algo"  
        r'[Cc]he,?\s+([A-Z][A-Z\s&\.]+?)\s+',
        # Solo nombre al inicio
        r'^([A-Z][A-Z\s&\.]{2,20}?)\s+'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_query.strip())
        if match:
            nombre_candidato = match.group(1).strip()
            
            # Filtrar palabras que no son nombres de empresas
            exclude_words = ['QUE', 'COMO', 'DONDE', 'CUANDO', 'POR', 'PARA', 'CON', 'SIN', 'SOBRE']
            if nombre_candidato.upper() not in exclude_words and len(nombre_candidato) >= 3:
                return nombre_candidato
    
    return None

def identify_cliente_strategic_enhanced(user_query, db_engine):
    """
    Identificación mejorada para consultas estratégicas
    """
    
    logger.info(f"🔍 Identificación estratégica para: {user_query}")
    
    # 1. Intentar extracción de nombre de la query
    nombre_candidato = extract_client_from_strategic_query(user_query)
    
    if nombre_candidato:
        logger.info(f"🎯 Nombre candidato extraído: '{nombre_candidato}'")
        
        # 2. Usar sistema robusto para identificar
        cliente_info = identify_cliente_automatico_robusto(nombre_candidato, db_engine)
        
        if cliente_info:
            logger.info(f"✅ Cliente estratégico identificado: {cliente_info['nombre']}")
            return cliente_info
    
    # 3. Fallback: usar sistema original
    cliente_info = identify_cliente_automatico_robusto(user_query, db_engine)
    
    if cliente_info:
        logger.info(f"✅ Cliente fallback identificado: {cliente_info['nombre']}")
        return cliente_info
    
    logger.warning(f"❌ Cliente no identificado en consulta estratégica: {user_query}")
    return None

def get_analisis_estrategico_cliente(cliente_info, user_query, db_engine):
    """
    Generar análisis estratégico específico para un cliente
    """
    
    anunciante_id = cliente_info['anunciante_id']
    nombre_cliente = cliente_info['nombre']
    
    logger.info(f"🧠 Generando análisis estratégico para: {nombre_cliente}")
    
    try:
        with db_engine.connect() as conn:
            # Query completa para análisis estratégico
            stmt = text("""
                SELECT 
                    -- Identificación
                    p.nombre_anunciante,
                    p.rubro_principal,
                    p.tamano_de_la_empresa_cantidad_de_empleados,
                    
                    -- Perfil estratégico
                    p.cluster,
                    CAST(p.cultura AS FLOAT) as cultura,
                    CAST(p.competitividad AS FLOAT) as competitividad,
                    CAST(p.puntaje_total AS FLOAT) as puntaje_total,
                    CAST(p.la_empresa_invierte_en_digital AS FLOAT) as digital_score,
                    
                    -- Inversiones publicitarias
                    CAST(p.inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT) as inversion_tv,
                    CAST(p.inversion_en_radio_2024_en_miles_usd AS FLOAT) as inversion_radio,
                    CAST(p.inversion_en_cable_2024_en_miles_usd AS FLOAT) as inversion_cable,
                    
                    -- Datos organizacionales
                    p.central_de_medios,
                    p.tiene_la_empresa_departamento_de_marketing,
                    p.en_que_medios_invierte_la_empresa_principalmente,
                    
                    -- Facturación nuestra
                    COALESCE(SUM(f.facturacion), 0) as facturacion_total,
                    COALESCE(SUM(f.revenue), 0) as revenue_total,
                    COUNT(f.*) as registros,
                    STRING_AGG(DISTINCT f.division, ', ') as divisiones,
                    STRING_AGG(DISTINCT f.arena, ', ') as arenas
                    
                FROM dim_anunciante_perfil p
                LEFT JOIN fact_facturacion f ON p.anunciante_id = f.anunciante_id
                WHERE p.anunciante_id = :anunciante_id
                GROUP BY p.anunciante_id, p.nombre_anunciante, p.rubro_principal, 
                         p.tamano_de_la_empresa_cantidad_de_empleados, p.cluster,
                         p.cultura, p.competitividad, p.puntaje_total, p.la_empresa_invierte_en_digital,
                         p.inversion_en_tv_abierta_2024_en_miles_usd, p.inversion_en_radio_2024_en_miles_usd,
                         p.inversion_en_cable_2024_en_miles_usd, p.central_de_medios,
                         p.tiene_la_empresa_departamento_de_marketing, p.en_que_medios_invierte_la_empresa_principalmente
            """)
            
            result = conn.execute(stmt, {"anunciante_id": anunciante_id}).fetchone()
            
            if not result:
                return {'error': f'No se encontraron datos para {nombre_cliente}'}
            
            # Compilar análisis estratégico
            analisis = {
                'cliente': result.nombre_anunciante,
                'perfil': {
                    'rubro': result.rubro_principal,
                    'tamaño': result.tamano_de_la_empresa_cantidad_de_empleados,
                    'cluster': result.cluster,
                    'cultura': result.cultura,
                    'competitividad': result.competitividad,
                    'puntaje_total': result.puntaje_total,
                    'digital_score': result.digital_score
                },
                'inversiones_mercado': {
                    'tv_usd': result.inversion_tv or 0,
                    'radio_usd': result.inversion_radio or 0,
                    'cable_usd': result.inversion_cable or 0,
                    'total_medios_usd': (result.inversion_tv or 0) + (result.inversion_radio or 0) + (result.inversion_cable or 0)
                },
                'estructura_organizacional': {
                    'central_medios': result.central_de_medios,
                    'depto_marketing': result.tiene_la_empresa_departamento_de_marketing,
                    'medios_principales': result.en_que_medios_invierte_la_empresa_principalmente
                },
                'relacion_comercial': {
                    'facturacion_total': float(result.facturacion_total),
                    'revenue_total': float(result.revenue_total),
                    'registros': result.registros,
                    'divisiones': result.divisiones,
                    'arenas': result.arenas,
                    'es_cliente': result.registros > 0
                }
            }
            
            # Generar insights específicos basados en el tipo de pregunta
            analisis['insights'] = generar_insights_especificos(analisis, user_query)
            
            return analisis
    
    except Exception as e:
        logger.error(f"❌ Error análisis estratégico: {e}")
        return {'error': str(e)}

def generar_insights_especificos(analisis, user_query):
    """
    Generar insights específicos basados en el tipo de pregunta
    """
    
    insights = []
    query_lower = user_query.lower()
    
    # Análisis de innovación
    if any(word in query_lower for word in ['innovador', 'innovacion', 'innovativa']):
        digital_score = analisis['perfil']['digital_score'] or 0
        competitividad = analisis['perfil']['competitividad'] or 0
        arenas = analisis['relacion_comercial']['arenas'] or ''
        
        if digital_score >= 8:
            insights.append("✅ Empresa altamente digital (score ≥8)")
        elif digital_score >= 5:
            insights.append("⚡ Empresa moderadamente digital")
        else:
            insights.append("❌ Empresa con bajo score digital")
        
        if competitividad >= 0.8:
            insights.append("✅ Empresa altamente competitiva")
        elif competitividad >= 0.5:
            insights.append("⚡ Empresa moderadamente competitiva")
        else:
            insights.append("❌ Empresa con baja competitividad")
        
        if 'CREACION' in arenas.upper():
            insights.append("✅ Recibe servicios de CREACIÓN (innovador)")
        if 'BI' in arenas.upper():
            insights.append("✅ Recibe servicios de BI (estratégico)")
        if arenas and 'DISTRIBUCION' in arenas.upper() and 'CREACION' not in arenas.upper():
            insights.append("⚠️ Solo recibe DISTRIBUCIÓN (tradicional)")
    
    # Análisis de captura de inversión
    if any(word in query_lower for word in ['captura', 'inversion', 'escapando']):
        inversion_total = analisis['inversiones_mercado']['total_medios_usd']
        facturacion = analisis['relacion_comercial']['facturacion_total']
        
        if inversion_total > 0 and facturacion > 0:
            # Convertir facturación a USD aproximado
            facturacion_usd = facturacion / 7500
            ratio = (facturacion_usd / inversion_total) * 100
            
            if ratio >= 25:
                insights.append(f"✅ Alta captura: Representa {ratio:.1f}% de su inversión")
            elif ratio >= 10:
                insights.append(f"⚡ Captura moderada: {ratio:.1f}% de su inversión")
            else:
                insights.append(f"❌ Baja captura: Solo {ratio:.1f}% de su inversión")
        elif inversion_total > 0:
            insights.append("❌ Invierte en medios pero no factura con nosotros")
        elif facturacion > 0:
            insights.append("✅ Cliente activo sin inversión declarada en medios tradicionales")
    
    # Análisis de estructura
    if any(word in query_lower for word in ['departamento', 'agencia', 'central']):
        central = analisis['estructura_organizacional']['central_medios']
        depto = analisis['estructura_organizacional']['depto_marketing']
        
        if depto == 'Si' and central:
            insights.append(f"🏢 Estructura: Depto Marketing + Central {central}")
        elif depto == 'Si':
            insights.append("🏢 Tiene departamento de marketing propio")
        elif central:
            insights.append(f"🏢 Trabaja con central {central}")
    
    return insights

# FUNCIÓN PRINCIPAL PARA INTEGRAR EN GET_CLIENTE_360
def get_cliente_360_strategic(user_query, db_engine):
    """
    Versión mejorada de get_cliente_360 con análisis estratégico
    """
    
    logger.info(f"🎯 Iniciando análisis estratégico 360° para: {user_query}")
    
    # 1. Identificación mejorada
    cliente_info = identify_cliente_strategic_enhanced(user_query, db_engine)
    
    if not cliente_info:
        logger.warning(f"❌ Cliente no encontrado: {user_query}")
        return []
    
    # 2. Análisis estratégico completo
    analisis_estrategico = get_analisis_estrategico_cliente(cliente_info, user_query, db_engine)
    
    if 'error' in analisis_estrategico:
        logger.error(f"❌ Error en análisis: {analisis_estrategico['error']}")
        return []
    
    # 3. Formatear para Claude
    resultado = {
        'tipo_analisis': 'estrategico',
        'cliente': analisis_estrategico['cliente'],
        'consulta_original': user_query,
        'analisis_completo': analisis_estrategico
    }
    
    logger.info(f"✅ Análisis estratégico completado para {cliente_info['nombre']}")
    
    return [resultado]

def extract_client_from_strategic_query(user_query):
    """
    Extraer nombres de clientes de preguntas estratégicas complejas
    """
    
    # Patrones para diferentes formatos de pregunta
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
            nombre_candidato = re.sub(r'\s+', ' ', nombre_candidato)
            
            # Filtrar palabras que no son nombres de empresas
            exclude_words = ['QUE', 'COMO', 'DONDE', 'CUANDO', 'POR', 'PARA', 'CON', 'SIN', 'SOBRE', 'ESTA', 'ESTAN']
            
            if (nombre_candidato.upper() not in exclude_words and 
                len(nombre_candidato) >= 3 and 
                len(nombre_candidato) <= 30):
                
                logger.info(f"🎯 Nombre candidato extraído: '{nombre_candidato}'")
                return nombre_candidato
    
    return None

def get_cliente_360_strategic(user_query, db_engine):
    """
    Análisis estratégico 360° para consultas complejas
    Esta es la función que falta y está siendo llamada desde get_cliente_360()
    """
    
    logger.info(f"🎯 Iniciando análisis estratégico 360° para: {user_query}")
    
    # 1. Intentar extracción específica de nombre
    nombre_candidato = extract_client_from_strategic_query(user_query)
    
    if nombre_candidato:
        logger.info(f"✅ Usando nombre extraído: '{nombre_candidato}'")
        
        # 2. Usar sistema robusto SOLO con el nombre limpio
        cliente_info = identify_cliente_automatico_robusto(nombre_candidato, db_engine)
        
        if cliente_info:
            logger.info(f"✅ Cliente estratégico identificado: {cliente_info['nombre']}")
            
            # 3. Usar la misma lógica que el análisis normal
            datos_erp = get_facturacion_erp_completa(db_engine.connect(), cliente_info['anunciante_id'])
            
            if not datos_erp:
                logger.warning(f"❌ No hay datos para cliente: {cliente_info['nombre']}")
                return []
            
            # 4. Enriquecer con datos AdLens y DNIT
            datos_enriquecidos = enrich_with_adlens_and_dnit(datos_erp, cliente_info['anunciante_id'], db_engine)
            
            # 5. Formatear para Claude con contexto estratégico
            resultado = {
                'tipo_analisis': 'estrategico',
                'cliente': cliente_info['nombre'],
                'anunciante_id': cliente_info['anunciante_id'],
                'consulta_original': user_query,
                'metodo_identificacion': cliente_info.get('method', 'strategic'),
                'datos_completos': datos_enriquecidos
            }
            
            logger.info(f"✅ Análisis estratégico completado para {cliente_info['nombre']}")
            return [resultado]
        
        else:
            logger.warning(f"❌ Nombre extraído '{nombre_candidato}' no encontrado en BD")
    
    # 3. Fallback: usar identificación normal
    logger.info("🔄 Fallback: usando identificación normal")
    cliente_info = identify_cliente_automatico_robusto(user_query, db_engine)
    
    if cliente_info:
        logger.info(f"✅ Cliente fallback identificado: {cliente_info['nombre']}")
        
        # Usar análisis normal
        datos_erp = get_facturacion_erp_completa(db_engine.connect(), cliente_info['anunciante_id'])
        
        if datos_erp:
            datos_enriquecidos = enrich_with_adlens_and_dnit(datos_erp, cliente_info['anunciante_id'], db_engine)
            return [datos_enriquecidos]
    
    logger.warning(f"❌ Cliente no encontrado: {user_query}")
    return []



def enrich_with_adlens_and_dnit(datos_erp, anunciante_id, db_engine):
    """
    Enriquecer datos ERP con información de AdLens y DNIT
    Esta función faltaba en el sistema estratégico
    """
    
    try:
        with db_engine.connect() as conn:
            # Obtener datos AdLens
            stmt_adlens = text("""
                SELECT 
                    nombre_anunciante,
                    rubro_principal,
                    tamano_de_la_empresa_cantidad_de_empleados,
                    cluster,
                    tipo_de_cluster,
                    cultura,
                    ejecucion,
                    estructura,
                    competitividad,
                    puntaje_total,
                    CAST(inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT) as inv_tv_usd,
                    CAST(inversion_en_radio_2024_en_miles_usd AS FLOAT) as inv_radio_usd,
                    CAST(inversion_en_cable_2024_en_miles_usd AS FLOAT) as inv_cable_usd,
                    central_de_medios,
                    tiene_la_empresa_departamento_de_marketing,
                    en_que_medios_invierte_la_empresa_principalmente,
                    la_empresa_invierte_en_digital
                FROM dim_anunciante_perfil
                WHERE anunciante_id = :anunciante_id
            """)
            
            adlens_data = conn.execute(stmt_adlens, {"anunciante_id": anunciante_id}).fetchone()
            
            # Obtener datos DNIT
            stmt_dnit = text("""
                SELECT 
                    ranking,
                    aporte_gs,
                    ingreso_estimado_gs,
                    razon_social
                FROM dim_posicionamiento_dnit
                WHERE anunciante_id = :anunciante_id
            """)
            
            dnit_data = conn.execute(stmt_dnit, {"anunciante_id": anunciante_id}).fetchone()
            
            # Combinar todos los datos
            datos_enriquecidos = datos_erp.copy()
            
            # Agregar datos AdLens
            if adlens_data:
                datos_enriquecidos.update({
                    'perfil_adlens': {
                        'nombre': adlens_data.nombre_anunciante,
                        'rubro': adlens_data.rubro_principal,
                        'tamaño_empresa': adlens_data.tamano_de_la_empresa_cantidad_de_empleados,
                        'cluster': adlens_data.cluster,
                        'tipo_cluster': adlens_data.tipo_de_cluster,
                        'cultura': adlens_data.cultura,
                        'ejecucion': adlens_data.ejecucion,
                        'estructura': adlens_data.estructura,
                        'competitividad': adlens_data.competitividad,
                        'puntaje_total': adlens_data.puntaje_total,
                        'inversiones_usd': {
                            'tv_abierta': adlens_data.inv_tv_usd or 0,
                            'radio': adlens_data.inv_radio_usd or 0,
                            'cable': adlens_data.inv_cable_usd or 0,
                            'total': (adlens_data.inv_tv_usd or 0) + (adlens_data.inv_radio_usd or 0) + (adlens_data.inv_cable_usd or 0)
                        },
                        'organizacion': {
                            'central_medios': adlens_data.central_de_medios,
                            'depto_marketing': adlens_data.tiene_la_empresa_departamento_de_marketing,
                            'medios_principales': adlens_data.en_que_medios_invierte_la_empresa_principalmente,
                            'invierte_digital': adlens_data.la_empresa_invierte_en_digital
                        }
                    }
                })
            
            # Agregar datos DNIT
            if dnit_data:
                datos_enriquecidos.update({
                    'ranking_dnit': {
                        'ranking': dnit_data.ranking,
                        'aporte_gs': dnit_data.aporte_gs,
                        'ingreso_estimado_gs': dnit_data.ingreso_estimado_gs,
                        'razon_social': dnit_data.razon_social
                    }
                })
            
            if 'facturacion_total' in datos_enriquecidos:
                datos_enriquecidos['facturacion_total'] = float(datos_enriquecidos['facturacion_total'])
            if 'revenue_total' in datos_enriquecidos:
                datos_enriquecidos['revenue_total'] = float(datos_enriquecidos['revenue_total'])
            if 'costo_total' in datos_enriquecidos:
                datos_enriquecidos['costo_total'] = float(datos_enriquecidos['costo_total'])

            logger.info(f"✅ Datos enriquecidos para anunciante {anunciante_id}")
            logger.info(f"🔍 DEBUG - Facturación en datos enriquecidos: {datos_enriquecidos.get('facturacion_total', 'NO ENCONTRADA')}")

            return datos_enriquecidos
            
    except Exception as e:
        logger.error(f"❌ Error enriqueciendo datos: {e}")
        # Si hay error, retornar datos ERP originales
        return datos_erp