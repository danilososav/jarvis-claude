import logging
from anthropic import Anthropic
from typing import Dict, Any


logger = logging.getLogger(__name__)

class ClaudeHandler:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-haiku-4-5-20251001"
        
    def enhance_response(self, user_query: str, data: list, query_type: str) -> str:
        """Mejorar respuesta con Claude"""
        
        system_prompt = """Eres JARVIS, asistente de BI para agencia de medios en Paraguay.
- Profesional pero accesible
- Español paraguayo (podés usar "vos")
- Breve: 2-4 oraciones máximo
- NUNCA inventes datos
- Números con formato: 21.228.763.493,72"""

        context_hints = {
            "ranking": "Top clientes con análisis de concentración",
            "facturacion": "Monto exacto, si es Top 5, observación relevante",
            "comparacion": "Diferencia %, ganador, estrategias diferenciadas",
            "perfil": "Características empresa, cluster, tamaño, potencial",
            "perfil_completo": "Integra facturación + perfil AdLens. Describe: rubro, tamaño, cluster, inversión en medios, digital, CRM, scores. Resume en 4-5 oraciones.",
        }
        
        hint = context_hints.get(query_type, "Responde clara y profesionalmente")
        
        user_message = f"""Usuario preguntó: "{user_query}"

Datos:
{str(data)}

Tipo: {query_type}
Instrucción: {hint}

Genera respuesta corporativa (2-4 oraciones)."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            logger.info(f"✅ Claude respondió: {query_type}")
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"❌ Error Claude: {e}")
            return None