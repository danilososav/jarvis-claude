"""
validate_feedback.py - Sistema de validación automática de feedback con Claude
"""

import logging
from datetime import datetime
import json
from claude_handler_v2 import ClaudeHandler

logger = logging.getLogger(__name__)


def validate_feedback_with_claude(feedback_data, claude_handler):
    """
    Valida feedback de trainer usando Claude API
    
    Args:
        feedback_data: dict con {
            'original_query': str,
            'original_response': str,
            'corrected_response': str,
            'data_snapshot': list - datos originales de la BD
        }
        claude_handler: instancia de ClaudeHandler
    
    Returns:
        dict con {
            'verdict': 'approved' | 'rejected',
            'reasoning': str,
            'is_factual': bool,
            'is_style': bool,
            'data_evidence': str,
            'trainer_message': str
        }
    """
    
    # Construir prompt para Claude
    prompt = build_validation_prompt(feedback_data)
    
    try:
        # Llamar a Claude con temperatura baja (más determinista)
        response = claude_handler.call_claude_raw(
            prompt=prompt,
            max_tokens=1500,
            temperature=0.2  # Bajo para ser más consistente
        )
        
        # Parsear respuesta JSON
        validation_result = parse_validation_response(response)
        
        logger.info(f"✅ Validación completada: verdict={validation_result['verdict']}")
        
        return validation_result
        
    except Exception as e:
        logger.error(f"❌ Error en validación con Claude: {e}")
        
        # Fallback: si Claude falla, marcar para revisión manual
        return {
            'verdict': 'rejected',  # Por seguridad, no auto-aprobar
            'reasoning': f'Error en validación automática: {str(e)}. Requiere revisión manual.',
            'is_factual': False,
            'is_style': False,
            'data_evidence': 'N/A',
            'trainer_message': 'Hubo un error técnico al validar tu corrección. El administrador fue notificado.'
        }


def build_validation_prompt(feedback_data):
    """Construye el prompt para que Claude valide el feedback"""
    
    # Formatear datos de la BD de forma legible
    data_str = json.dumps(feedback_data['data_snapshot'], indent=2, ensure_ascii=False)
    
    prompt = f"""Eres un validador de respuestas de Business Intelligence. Un entrenador (trainer) ha corregido una de tus respuestas anteriores. Debes validar si la corrección es apropiada basándote en los datos reales.

QUERY ORIGINAL DEL USUARIO:
"{feedback_data['original_query']}"

TU RESPUESTA ORIGINAL:
"{feedback_data['original_response']}"

CORRECCIÓN PROPUESTA POR TRAINER:
"{feedback_data['corrected_response']}"

DATOS REALES DE LA BASE DE DATOS:
{data_str}

INSTRUCCIONES:
1. Compara tu respuesta original con los datos reales de la base de datos
2. Compara la corrección del trainer con los datos reales
3. Determina si la corrección es:
   - FACTUALMENTE correcta (números, nombres, datos coinciden con la BD)
   - FACTUALMENTE incorrecta (contradice los datos de la BD)
   - De ESTILO/FORMATO (opinión sobre redacción, tono, formato)

REGLAS DE VALIDACIÓN:
- Si la corrección ES FACTUALMENTE CORRECTA según los datos → verdict: "approved"
- Si la corrección ES FACTUALMENTE INCORRECTA según los datos → verdict: "rejected"
- Si ambas versiones son factualmente correctas pero difieren en estilo → verdict: "rejected" (mantener consistencia)
- Si no estás 100% seguro → verdict: "rejected" (por seguridad)

Responde ÚNICAMENTE con un objeto JSON (sin markdown, sin backticks) en este formato exacto:
{{
  "verdict": "approved",
  "reasoning": "Explicación técnica detallada de tu análisis",
  "is_factual": true,
  "is_style": false,
  "data_evidence": "Cita los datos específicos de la BD que usaste para decidir",
  "trainer_message": "Mensaje claro y amigable para el trainer explicando tu decisión"
}}

IMPORTANTE: 
- En "trainer_message" usa tono profesional pero amigable
- Si rechazas, explica POR QUÉ la respuesta original es correcta
- Si apruebas, reconoce el error y agradece la corrección
- Cita siempre los números/datos específicos de la BD"""

    return prompt


def parse_validation_response(response_text):
    """Parsea la respuesta JSON de Claude"""
    
    try:
        # Limpiar respuesta (por si Claude agrega texto extra)
        response_text = response_text.strip()
        
        # Buscar JSON en la respuesta
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)
            
            # Validar campos requeridos
            required_fields = ['verdict', 'reasoning', 'is_factual', 'is_style', 'data_evidence', 'trainer_message']
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Campo requerido faltante: {field}")
            
            # Validar verdict
            if result['verdict'] not in ['approved', 'rejected']:
                raise ValueError(f"Verdict inválido: {result['verdict']}")
            
            return result
        else:
            raise ValueError("No se encontró JSON en la respuesta")
            
    except Exception as e:
        logger.error(f"Error parseando respuesta de Claude: {e}")
        logger.error(f"Respuesta recibida: {response_text}")
        raise


def format_validation_for_trainer(validation_result):
    """
    Formatea el resultado de validación para mostrarlo al trainer
    
    Returns:
        dict con {
            'status': 'approved' | 'rejected',
            'title': str,
            'message': str,
            'show_escalate_button': bool
        }
    """
    
    if validation_result['verdict'] == 'approved':
        return {
            'status': 'approved',
            'title': '✅ Corrección Aplicada',
            'message': validation_result['trainer_message'],
            'show_escalate_button': False
        }
    else:
        return {
            'status': 'rejected',
            'title': '❌ Corrección No Aplicada',
            'message': validation_result['trainer_message'],
            'details': validation_result['reasoning'],
            'show_escalate_button': True
        }
