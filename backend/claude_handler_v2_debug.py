"""
Claude Handler v2 - Análisis BI Profesional Completo
Sistema que entiende español paraguayo pero responde con análisis corporativo detallado
"""

import logging
from anthropic import Anthropic, RateLimitError, APIError
from typing import Dict, List, Any
import time

logger = logging.getLogger(__name__)


class ClaudeHandler:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"  # Sonnet 4.5
        
    def enhance_response(
        self, 
        user_query: str, 
        data: List[Dict], 
        query_type: str,
        max_retries: int = 3
    ) -> str:
        """
        Genera respuesta analítica profesional completa
        - Entiende: español paraguayo coloquial (capa 8)
        - Responde: análisis BI profesional detallado
        """
        
        for attempt in range(max_retries):
            try:
                prompt = self._build_prompt(user_query, data, query_type)
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    temperature=0.3,
                    system=self._get_system_prompt(),
                    print(f'🔍 PROMPT A CLAUDE: {messages}')
                    print(f'🔍 USER PROMPT: {content if "content" in locals() else "content not found"}')
                    messages=[{"role": "user", "content": prompt}]
                )
                
                logger.info(f"✅ Claude Sonnet respondió: {query_type}")
                return response.content[0].text.strip()
                
            except RateLimitError:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"⏳ Rate limit, esperando {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return self._fallback_response(query_type, data)
                    
            except APIError as e:
                logger.error(f"❌ Error API Claude: {e}")
                return self._fallback_response(query_type, data)
    
    def call_claude_raw(self, prompt: str, max_tokens: int = 1500, temperature: float = 0.2) -> str:
        """
        Llamada directa a Claude API sin procesamiento adicional
        Usado para validación de feedback
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                print(f'🔍 PROMPT A CLAUDE: {messages}')
                print(f'🔍 USER PROMPT: {content if "content" in locals() else "content not found"}')
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except RateLimitError:
            logger.error("❌ Rate limit en call_claude_raw")
            raise
        except APIError as e:
            logger.error(f"❌ API Error en call_claude_raw: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado en call_claude_raw: {e}")
            raise
    
    def _get_system_prompt(self) -> str:
        """System prompt: Define personalidad y comportamiento"""
        return """Eres JARVIS, el sistema de Business Intelligence de una agencia de medios y publicidad en Paraguay.

CAPACIDADES DE COMPRENSIÓN:
- Entiendes español paraguayo coloquial, jerga local y expresiones informales
- Comprendes queries de usuarios "capa 8" (usuarios no técnicos, coloquiales)
- Interpretas preguntas ambiguas, mal escritas o con errores gramaticales

ESTILO DE RESPUESTA:
- Análisis profesional COMPLETO y detallado
- Tono corporativo pero claro y accesible
- Sin emojis, sin jerga paraguaya en la respuesta
- Estructura: contexto → datos → insights → recomendaciones

FORMATO DE NÚMEROS:
- Guaraníes: 150.000.000 Gs o 150M Gs
- Porcentajes: 34,5%
- Evita notación científica

LONGITUD DE RESPUESTA SEGÚN COMPLEJIDAD:
- Queries simples (facturación 1 cliente): 3-4 oraciones concisas
- Rankings básicos: 4-5 oraciones con contexto
- Comparaciones: 5-6 oraciones analizando diferencias
- Análisis complejos: 8-12 oraciones con insights profundos
- Perfiles completos: 10-15 oraciones integrando múltiples dimensiones

PRINCIPIOS CRÍTICOS:
1. NUNCA inventes datos que no estén en la información proporcionada
2. Si los datos son insuficientes, indícalo claramente
3. Siempre contextualiza los números (market share, promedios, comparaciones)
4. Identifica patrones, tendencias y anomalías relevantes
5. Concluye con recomendaciones accionables cuando sea pertinente

ESTRUCTURA TÍPICA DE RESPUESTA:
1. Respuesta directa a la pregunta
2. Contexto y datos clave
3. Análisis de patrones o comparaciones
4. Insights estratégicos
5. Recomendaciones (si aplica)"""

    def _build_prompt(self, user_query: str, data: List[Dict], query_type: str) -> str:
        """Construye el prompt según el tipo de query"""
        
        # Formatear datos de forma legible
        data_formatted = self._format_data(data, query_type)
        
        # Instrucciones específicas por tipo
        instructions = self._get_type_instructions(query_type)
        
        return f"""QUERY DEL USUARIO:
"{user_query}"

DATOS DISPONIBLES:
{data_formatted}

TIPO DE ANÁLISIS: {query_type}

INSTRUCCIONES ESPECÍFICAS:
{instructions}

Genera una respuesta analítica profesional completa que responda directamente a la pregunta del usuario."""

    def _format_data(self, data: List[Dict], query_type: str) -> str:
        """Formatea los datos de forma estructurada"""
        if not data:
            return "No hay datos disponibles"
        
        if query_type == "ranking":
            lines = []
            for i, item in enumerate(data, 1):
                cliente = item.get('cliente', 'N/A')
                fac = item.get('facturacion', 0)
                ms = item.get('market_share', 0)
                lines.append(f"{i}. {cliente}: {fac:,.0f} Gs ({ms:.2f}% market share)")
            return "\n".join(lines)
        
        elif query_type == "facturacion":
            item = data[0] if data else {}
            return f"""Cliente: {item.get('cliente', 'N/A')}
Facturación Total: {item.get('facturacion', 0):,.0f} Gs
Promedio Mensual: {item.get('promedio_mensual', 0):,.0f} Gs
Market Share: {item.get('market_share', 0):.2f}%
Registros: {item.get('registros', 0)}"""
        
        elif query_type == "comparacion":
            if len(data) >= 2:
                c1, c2 = data[0], data[1]
                return f"""CLIENTE A: {c1.get('cliente', 'N/A')}
Facturación: {c1.get('facturacion', 0):,.0f} Gs
Market Share: {c1.get('market_share', 0):.2f}%

CLIENTE B: {c2.get('cliente', 'N/A')}
Facturación: {c2.get('facturacion', 0):,.0f} Gs
Market Share: {c2.get('market_share', 0):.2f}%"""
        
        else:
            # Formato genérico para otros tipos
            return "\n".join([str(item) for item in data[:10]])
    
    def _get_type_instructions(self, query_type: str) -> str:
        """Instrucciones específicas por tipo de query"""
        
        instructions = {
            "ranking": """
- Presenta el ranking completo con contexto
- Identifica el líder y su ventaja sobre el segundo lugar
- Calcula concentración: ¿qué % representan los top 3 o top 5?
- Señala brechas significativas entre posiciones
- Si hay patrones (ej: dominio de cierto sector), menciónalo""",
            
            "facturacion": """
- Responde directamente cuánto facturó
- Contextualiza: ¿es un cliente top? ¿qué posición ocupa?
- Analiza su market share: ¿es relevante?
- Compara promedio mensual vs total para identificar estacionalidad
- Menciona número de registros (años/meses activo)""",
            
            "comparacion": """
- Calcula diferencia absoluta y porcentual entre clientes
- Identifica quién es el ganador y por cuánto
- Analiza disparidad en market share
- Busca patrones: ¿ambos son top 10? ¿uno domina por mucho?
- Sugiere posibles razones estratégicas (tamaño, sector, etc.)""",
            
            "perfil": """
- Resume características clave del cliente
- Integra datos de facturación + perfil AdLens
- Identifica cluster y posicionamiento
- Analiza potencial y oportunidades
- Señala riesgos o limitaciones si existen""",
            
            "perfil_completo": """
- Análisis integral: facturación + perfil + comportamiento
- Cluster y características estratégicas
- Inversión en medios (TV, digital, radio, etc.)
- Scores de competitividad y proyección
- Recomendaciones de acercamiento comercial""",
            
            "trend": """
- Describe evolución temporal clara
- Identifica tendencia: crecimiento, decrecimiento, estabilidad
- Calcula variación porcentual total y CAGR si aplica
- Señala picos, valles y puntos de inflexión
- Contextualiza: ¿es normal o anómalo?""",
            
            "dynamic_table": """
- Resume qué información contiene la tabla
- Señala número de registros encontrados
- Identifica patrones o datos relevantes
- Si es tabla de clientes, contextualiza facturación o perfil""",
            
            "chart": """
- Resume el insight principal que muestra el gráfico
- Identifica los 2-3 elementos más destacados
- Menciona tendencias visuales evidentes
- Contextualiza las diferencias entre elementos""",
            
            "generico": """
- Analiza la información disponible
- Identifica patrones o insights relevantes
- Presenta conclusiones claras
- Sugiere análisis complementarios si son pertinentes"""
        }
        
        return instructions.get(query_type, instructions["generico"])
    
    def _fallback_response(self, query_type: str, data: List[Dict]) -> str:
        """Respuesta de emergencia si Claude API falla"""
        if not data:
            return "No se encontraron datos para esta consulta."
        
        if query_type == "ranking":
            total = sum(r.get("facturacion", 0) for r in data)
            return f"Se encontraron {len(data)} clientes con una facturación total de {total:,.0f} Gs. El sistema está experimentando alta demanda, intenta nuevamente."
        
        elif query_type == "facturacion":
            if data:
                r = data[0]
                return f"{r.get('cliente', 'Cliente')} registró una facturación de {r.get('facturacion', 0):,.0f} Gs."
        
        return "Consulta procesada. El sistema está experimentando alta demanda, intenta nuevamente para obtener análisis detallado."