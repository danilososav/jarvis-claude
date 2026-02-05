"""
JARVIS - Búsqueda flexible entre múltiples fuentes de datos
Funciones para consultar facturación, inversión en medios, ranking DNIT y perfiles AdLens
"""

from sqlalchemy import text
from fuzzywuzzy import fuzz
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def convert_decimals_to_float(data):
    """Convierte objetos Decimal a float para serialización JSON"""
    if isinstance(data, list):
        return [convert_decimals_to_float(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_decimals_to_float(v) for k, v in data.items()}
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return data

def buscar_anunciante(nombre_cliente, engine):
    """
    Busca anunciante_id usando fuzzy matching
    """
    try:
        with engine.connect() as conn:
            # Buscar directo primero
            result = conn.execute(text("""
                SELECT anunciante_id, nombre_canonico 
                FROM dim_anunciante 
                WHERE UPPER(nombre_canonico) LIKE :nombre
            """), {'nombre': f'%{nombre_cliente.upper()}%'}).fetchone()
            
            if result:
                return result._asdict()
            
            # Buscar en aliases
            result = conn.execute(text("""
                SELECT a.anunciante_id, a.nombre_canonico
                FROM dim_anunciante_aliases alias
                JOIN dim_anunciante a ON alias.anunciante_id = a.anunciante_id
                WHERE UPPER(alias.nombre_alias) LIKE :nombre
                ORDER BY alias.confianza DESC
                LIMIT 1
            """), {'nombre': f'%{nombre_cliente.upper()}%'}).fetchone()
            
            if result:
                return result._asdict()
                
    except Exception as e:
        logger.error(f"Error buscando anunciante {nombre_cliente}: {e}")
    
    return None


def get_facturacion_cliente(cliente_nombre, engine):
    """
    Obtiene facturación de un cliente con búsqueda flexible
    """
    try:
        # Buscar anunciante_id
        anunciante = buscar_anunciante(cliente_nombre, engine)
        
        if not anunciante:
            logger.warning(f"Cliente {cliente_nombre} no encontrado en dim_anunciante")
            return []
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    a.nombre_canonico as cliente,
                    COUNT(*) as periodos,
                    ROUND(SUM(f.facturacion), 2) as facturacion_total,
                    ROUND(AVG(f.facturacion), 2) as promedio_mensual,
                    ROUND(
                        SUM(f.facturacion) * 100.0 / 
                        (SELECT SUM(facturacion) FROM fact_facturacion), 
                        2
                    ) as market_share,
                    MIN(f.anio) as anio_inicio,
                    MAX(f.anio) as anio_fin
                FROM fact_facturacion f
                JOIN dim_anunciante a ON f.anunciante_id = a.anunciante_id
                WHERE f.anunciante_id = :anunciante_id
                GROUP BY a.anunciante_id, a.nombre_canonico
            """), {'anunciante_id': anunciante['anunciante_id']}).fetchall()
            
            return convert_decimals_to_float([dict(row._mapping) for row in result])
            
    except Exception as e:
        logger.error(f"Error obteniendo facturación de {cliente_nombre}: {e}")
        return []


def get_inversion_medios_cliente(cliente_nombre, engine, filtros=None):
    """
    Obtiene inversión en medios de un cliente con filtros opcionales
    filtros = {'medio': 'TV'} para filtrar por medio específico
    """
    try:
        # Buscar anunciante_id
        anunciante = buscar_anunciante(cliente_nombre, engine)
        
        if not anunciante:
            # Si no está en dim_anunciante, buscar directo en fact_inversion_medios
            logger.warning(f"Cliente {cliente_nombre} no encontrado en dim_anunciante, buscando directo en inversión")
            
            where_clause = "UPPER(nombre_anunciante) LIKE :cliente_nombre"
            params = {'cliente_nombre': f'%{cliente_nombre.upper()}%'}
            
            # Agregar filtros de medio si los hay
            if filtros and 'medio' in filtros:
                where_clause += " AND UPPER(medio) LIKE :filtro_medio"
                params['filtro_medio'] = f'%{filtros["medio"].upper()}%'
            
            with engine.connect() as conn:
                result = conn.execute(text(f"""
                    SELECT 
                        nombre_anunciante as cliente,
                        medio,
                        COUNT(*) as registros,
                        ROUND(SUM(monto_usd), 2) as inversion_usd,
                        ROUND(SUM(monto_gs), 2) as inversion_gs,
                        2024 as anio
                    FROM fact_inversion_medios
                    WHERE {where_clause}
                    GROUP BY nombre_anunciante, medio
                    ORDER BY inversion_usd DESC
                """), params).fetchall()
                
                return convert_decimals_to_float([dict(row._mapping) for row in result])
        
        # Si existe en dim_anunciante, buscar por anunciante_id
        where_clause = "anunciante_id = :anunciante_id"
        params = {'anunciante_id': anunciante['anunciante_id']}
        
        # Agregar filtros de medio si los hay
        if filtros and 'medio' in filtros:
            where_clause += " AND UPPER(medio) LIKE :filtro_medio"
            params['filtro_medio'] = f'%{filtros["medio"].upper()}%'
        
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT 
                    :nombre_cliente as cliente,
                    medio,
                    COUNT(*) as registros,
                    ROUND(SUM(monto_usd), 2) as inversion_usd,
                    ROUND(SUM(monto_gs), 2) as inversion_gs,
                    2024 as anio
                FROM fact_inversion_medios
                WHERE {where_clause}
                GROUP BY medio
                ORDER BY inversion_usd DESC
            """), {**params, 'nombre_cliente': anunciante['nombre_canonico']}).fetchall()
            
            return convert_decimals_to_float([dict(row._mapping) for row in result])
            
    except Exception as e:
        logger.error(f"Error obteniendo inversión de {cliente_nombre}: {e}")
        return []


def get_ranking_dnit_cliente(cliente_nombre, engine):
    """
    Obtiene ranking DNIT de un cliente
    """
    try:
        # Buscar anunciante_id primero
        anunciante = buscar_anunciante(cliente_nombre, engine)
        
        if anunciante:
            # Buscar por anunciante_id si existe
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT 
                        d.ranking,
                        d.razon_social as cliente,
                        d.aporte_gs,
                        d.ruc,
                        'matched' as status
                    FROM dim_posicionamiento_dnit d
                    WHERE d.anunciante_id = :anunciante_id
                """), {'anunciante_id': anunciante['anunciante_id']}).fetchall()
                
                if result:
                    return convert_decimals_to_float([dict(row._mapping) for row in result])
        
        # Si no encuentra por anunciante_id, buscar directo por nombre
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    ranking,
                    razon_social as cliente,
                    aporte_gs,
                    ruc,
                    'direct_match' as status
                FROM dim_posicionamiento_dnit
                WHERE UPPER(razon_social) LIKE :cliente_nombre
                ORDER BY ranking
                LIMIT 1
            """), {'cliente_nombre': f'%{cliente_nombre.upper()}%'}).fetchall()
            
            return convert_decimals_to_float([dict(row._mapping) for row in result])
            
    except Exception as e:
        logger.error(f"Error obteniendo ranking DNIT de {cliente_nombre}: {e}")
        return []


def get_perfil_adlens_cliente(cliente_nombre, engine):
    """
    Obtiene perfil AdLens de un cliente
    """
    try:
        # Buscar anunciante_id
        anunciante = buscar_anunciante(cliente_nombre, engine)
        
        if not anunciante:
            logger.warning(f"Cliente {cliente_nombre} no encontrado para perfil AdLens")
            return []
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    p.*,
                    a.nombre_canonico as cliente
                FROM dim_anunciante_perfil p
                JOIN dim_anunciante a ON p.anunciante_id = a.anunciante_id
                WHERE p.anunciante_id = :anunciante_id
            """), {'anunciante_id': anunciante['anunciante_id']}).fetchall()
            
            return convert_decimals_to_float([dict(row._mapping) for row in result])
            
    except Exception as e:
        logger.error(f"Error obteniendo perfil AdLens de {cliente_nombre}: {e}")
        return []