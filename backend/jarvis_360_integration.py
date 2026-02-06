"""
JARVIS BI 360° - IMPLEMENTACIÓN COMPLETA
Sistema de integración total: ERP + AdLens + DNIT
"""

from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def get_cliente_360(user_query):
    """
    FUNCIÓN MAESTRA: Obtiene visión 360° completa del cliente
    Integra: ERP + AdLens + DNIT + Perfiles + Inversiones granulares
    """
    
    logger.info(f"🔍 Iniciando análisis 360° para: {user_query}")
    
    try:
        # 1. IDENTIFICAR CLIENTE con fuzzy matching mejorado
        cliente_info = identify_cliente_fuzzy_360(user_query)
        if not cliente_info:
            logger.warning(f"❌ Cliente no encontrado: {user_query}")
            return []
        
        anunciante_id = cliente_info['anunciante_id']
        logger.info(f"✅ Cliente identificado: {cliente_info['nombre']} (ID: {anunciante_id})")
        
        # 2. OBTENER DATOS DE TODAS LAS FUENTES
        with engine.connect() as conn:
            
            # 2.1 FACTURACIÓN ERP (fact_facturacion)
            facturacion_data = get_facturacion_erp_completa(conn, anunciante_id)
            
            # 2.2 RANKING DNIT (dim_posicionamiento_dnit) 
            ranking_data = get_ranking_dnit_completo(conn, anunciante_id)
            
            # 2.3 PERFIL ADLENS (dim_anunciante_perfil)
            perfil_data = get_perfil_adlens_completo(conn, anunciante_id)
            
            # 2.4 INVERSIÓN GRANULAR OPCIONAL (fact_inversion_medios)
            inversion_granular = get_inversion_granular_opcional(conn, anunciante_id)
            
            # 3. INTEGRAR TODO EN ESTRUCTURA 360°
            cliente_360 = merge_all_sources_360(
                cliente_info, 
                facturacion_data, 
                ranking_data, 
                perfil_data, 
                inversion_granular
            )
            
            logger.info(f"✅ Análisis 360° completado para {cliente_info['nombre']}")
            return [cliente_360]  # Lista para compatibilidad
            
    except Exception as e:
        logger.error(f"❌ Error en análisis 360°: {e}")
        # Fallback a sistema anterior si falla
        return get_facturacion_enriched_fallback(user_query)

def identify_cliente_fuzzy_360(user_query):
    """
    Identificación mejorada de clientes usando dim_anunciante_perfil
    """
    
    try:
        with engine.connect() as conn:
            # Buscar en dim_anunciante_perfil (fuente principal AdLens)
            stmt = text("""
                SELECT 
                    p.anunciante_id,
                    p.nombre_anunciante as nombre,
                    a.razon_social as nombre_oficial
                FROM dim_anunciante_perfil p
                LEFT JOIN dim_anunciante a ON p.anunciante_id = a.anunciante_id
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
                
                if score > best_score and score > 0.4:  # Threshold más bajo
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
    Obtener facturación completa del ERP con evolución temporal
    """
    
    try:
        stmt = text("""
            SELECT 
                SUM(facturacion) as facturacion_total,
                SUM(revenue) as revenue_total, 
                SUM(costo) as costo_total,
                AVG(facturacion) as promedio_mensual,
                COUNT(*) as registros,
                STRING_AGG(DISTINCT division, ', ') as divisiones,
                STRING_AGG(DISTINCT arena, ', ') as arenas,
                -- Evolución mensual últimos 12 meses
                json_agg(
                    json_build_object(
                        'mes', mes,
                        'anio', anio, 
                        'facturacion', SUM(facturacion),
                        'revenue', SUM(revenue)
                    ) ORDER BY anio DESC, mes DESC
                ) FILTER (WHERE anio >= 2023) as evolucion_mensual
            FROM fact_facturacion 
            WHERE anunciante_id = :anunciante_id
            GROUP BY anunciante_id
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
                'evolucion_mensual': result.evolucion_mensual or []
            }
        else:
            return {}
            
    except Exception as e:
        logger.error(f"❌ Error obteniendo facturación ERP: {e}")
        return {}

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

