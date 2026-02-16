"""
SISTEMA DE CONSULTAS COMPLEJAS SIN CLAUDE
Explorar todas las capacidades del sistema 360° sin usar créditos
"""

from sqlalchemy import text
import json
import logging

logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    print("🚀 SISTEMA CONSULTAS COMPLEJAS SIN CLAUDE")
    print("="*60)
    print("✅ Comparaciones: 'comparar unilever vs nestle'")
    print("✅ Rankings: 'top 10 con clusters y medios'")
    print("✅ Clusters: 'analisis por clusters'")  
    print("✅ Completos: 'datos completos unilever'")
    print("✅ Estadísticas: 'estadisticas del mercado'")
    print("✅ Sin usar créditos de Claude API")

