"""
Integración con Claude API - Generador de SQL dinámico
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from sqlalchemy import text

logger = logging.getLogger(__name__)

# Cargar .env al inicio
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    logger.info(f"✅ .env cargado desde {env_path}")

API_KEY = os.getenv('CLAUDE_API_KEY')
if not API_KEY:
    logger.error("❌ CLAUDE_API_KEY no configurada")

def handle_query_with_claude(engine, user_query, user_id):
    """
    Genera SQL con Claude API y lo ejecuta.
    """
    if not API_KEY:
        return {
            "success": False,
            "response": "Error: API key no configurada",
            "query_type": "error",
            "rows": []
        }
    
    try:
        # Inicializar cliente
        client = anthropic.Anthropic(api_key=API_KEY)
        
        logger.info(f"🤖 Claude: {user_query[:80]}")
        
        # Schema para Claude
        db_schema = """TABLAS:
1. fact_facturacion: cliente_original, facturacion, arena, anio, mes
2. dim_anunciante_perfil: nombre_anunciante, cluster, con_respecto_al_marketing_y_la_publicidad_es_una_e, inversion_en_tv_abierta_2024_en_miles_usd, inversion_en_radio_2024_en_miles_usd, inversion_en_cable_2024_en_miles_usd, inversion_en_pdv_2024_en_miles_usd, inversion_en_medios, tiene_la_empresa_departamento_de_marketing, que_tan_desconfiada_es_la_empresa_cuanto_cuesta_ve, puntaje_total, competitividad, cultura, estructura, ejecucion, inversion
3. dim_mapeo_base_adlens: cliente_base, anunciante_adlens, similitud

JOIN CORRECTO:
FROM fact_facturacion f
LEFT JOIN dim_mapeo_base_adlens m ON LOWER(TRIM(f.cliente_original)) = LOWER(TRIM(m.cliente_base))
LEFT JOIN dim_anunciante_perfil p ON LOWER(TRIM(p.nombre_anunciante)) = LOWER(TRIM(m.anunciante_adlens))
WHERE f.facturacion > 0
"""
        
        prompt = f"""Eres experto en SQL PostgreSQL para análisis BI.

SCHEMA:
{db_schema}

QUERY: {user_query}

Genera SQL VÁLIDO. IMPORTANTE:
- Usa siempre dim_mapeo_base_adlens para joinear
- LOWER(TRIM()) para texto
- COALESCE para NULLs
- Castea NULLIF para text numéricos
- Retorna SOLO JSON sin explicaciones

{{"success": true, "sql": "...", "query_type": "ranking|facturacion|analisis_completo|..."}}
O si error: {{"success": false, "error": "..."}}
"""
        
        # Llamar a Claude
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        logger.info(f"✅ Respuesta Claude: {response_text[:100]}")
        
        # Parsear JSON
        try:
            result = json.loads(response_text)
        except:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                logger.error(f"❌ No se pudo parsear: {response_text}")
                return {
                    "success": False,
                    "response": "Error procesando respuesta",
                    "query_type": "error",
                    "rows": []
                }
        
        if not result.get("success"):
            logger.error(f"❌ Error Claude: {result.get('error')}")
            return {
                "success": False,
                "response": f"Error: {result.get('error')}",
                "query_type": "error",
                "rows": []
            }
        
        sql = result.get("sql")
        query_type = result.get("query_type", "general")
        
        # Ejecutar SQL
        try:
            with engine.connect() as conn:
                stmt = text(sql)
                db_result = conn.execute(stmt)
                rows = [dict(row._mapping) for row in db_result]
            
            logger.info(f"✅ {query_type}: {len(rows)} filas")
            
            # Formatear respuesta
            response_text = format_response(query_type, rows, user_query)
            
            return {
                "success": True,
                "response": response_text,
                "query_type": query_type,
                "rows": rows
            }
            
        except Exception as sql_err:
            logger.error(f"❌ SQL Error: {sql_err}")
            logger.error(f"SQL: {sql}")
            return {
                "success": False,
                "response": f"Error SQL: {str(sql_err)}",
                "query_type": "error",
                "rows": []
            }
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "success": False,
            "response": f"Error: {str(e)}",
            "query_type": "error",
            "rows": []
        }

def format_response(query_type, rows, user_query):
    """Formatea respuesta según query_type"""
    if not rows:
        return "📊 No hay datos disponibles para este análisis."
    
    if query_type == "ranking":
        response = "🏆 **Top Clientes**\n\n"
        for i, row in enumerate(rows[:5], 1):
            cliente = row.get('cliente') or row.get('cliente_original') or 'N/A'
            facturacion = row.get('facturacion') or row.get('facturacion_total') or 0
            response += f"{i}. **{cliente}** - {facturacion:,.0f} Gs\n"
        return response
    
    elif query_type == "facturacion":
        row = rows[0]
        cliente = row.get('cliente') or row.get('cliente_original') or 'N/A'
        facturacion = row.get('facturacion') or row.get('facturacion_total') or 0
        return f"💰 **{cliente}** facturó **{facturacion:,.0f} Gs**"
    
    elif query_type == "analisis_completo":
        response = "📊 **Análisis Completo**\n\n"
        row = rows[0]
        cliente = row.get('cliente') or row.get('nombre_anunciante') or 'N/A'
        facturacion = row.get('facturacion_total') or row.get('facturacion') or 0
        cluster = row.get('cluster') or 'N/A'
        response += f"**{cliente}**\n"
        response += f"💰 Facturación: {facturacion:,.0f} Gs\n"
        response += f"🎯 Cluster: {cluster}\n"
        if row.get('inversion_tv'):
            response += f"📺 TV: ${row.get('inversion_tv', 0):,.0f}k USD\n"
        if row.get('inversion_pdv'):
            response += f"🏪 PDV: ${row.get('inversion_pdv', 0):,.0f}k USD\n"
        return response
    
    elif query_type == "cluster":
        response = "🎯 **Clientes por Cluster**\n\n"
        for row in rows[:10]:
            cliente = row.get('cliente') or row.get('nombre_anunciante') or 'N/A'
            facturacion = row.get('facturacion') or 0
            response += f"- {cliente}: {facturacion:,.0f} Gs\n"
        return response
    
    else:
        response = f"📈 **{query_type.upper()}**\n\n"
        for row in rows[:5]:
            response += f"- {str(row)}\n"
        return response
