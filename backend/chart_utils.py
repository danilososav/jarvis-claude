"""
Utilidades para detección y generación de configuración de gráficos
Sistema que separa completamente gráficos de análisis de texto
"""

import logging

logger = logging.getLogger(__name__)


def detect_query_intent(user_query):
    """
    Detecta la intención del usuario:
    - chart_only: Solo gráfico
    - text_only: Solo análisis
    - chart_and_text: Ambos separados
    - table_only: Solo tabla
    - kpi_only: Solo KPI/cuadro de resultados
    """
    query_lower = user_query.lower()
    
    # Keywords de gráficos
    chart_keywords = [
        'gráfico', 'grafico', 'chart', 
        'visualiz', 'gráfica', 'grafica',
        'mostrar en gráfico', 'mostrame en gráfico',
        'barra', 'barras', 'bar',
        'línea', 'linea', 'line',
        'torta', 'pie', 'circular',
        'donut', 'dona', 'rosquilla',
        'horizontal', 'burbuja', 'burbujas', 'bubble',
        'scatter', 'dispersión', 'dispersion',
        'gauge', 'indicador', 'velocímetro', 'velocimetro',
        'radial'
    ]
    
    # Keywords de tabla
    table_keywords = [
        'tabla', 'table', 'listado', 'lista detallada',
        'en tabla', 'formato tabla', 'mostrame en tabla'
    ]
    
    # Keywords de KPI/cuadro
    kpi_keywords = [
        'kpi', 'métrica', 'metrica', 'indicador',
        'cuadro', 'resumen', 'dashboard',
        'tarjeta', 'card', 'resultado'
    ]
    
    # Keywords de análisis
    analysis_keywords = [
        'análisis', 'analisis', 'analyze',
        'explicame', 'explicación', 'explicacion',
        'detalle', 'detallado', 'profund',
        'por qué', 'porque', 'razón'
    ]
    
    has_chart = any(kw in query_lower for kw in chart_keywords)
    has_table = any(kw in query_lower for kw in table_keywords)
    has_kpi = any(kw in query_lower for kw in kpi_keywords)
    has_analysis = any(kw in query_lower for kw in analysis_keywords)
    
    # Detección de "y" o "también" que indica ambos
    has_both_connector = any(word in query_lower for word in [' y ', ' e ', ' también', ' tambien', ' además', ' ademas'])
    
    # Prioridad de detección
    if has_table and not has_chart:
        return "table_only"
    elif has_kpi and not has_chart and not has_table:
        return "kpi_only"
    elif has_chart and has_analysis:
        return "chart_and_text"
    elif has_chart and has_both_connector:
        return "chart_and_text"
    elif has_chart:
        return "chart_only"
    else:
        return "text_only"


def detect_chart_type(user_query):
    """
    Detecta el tipo de gráfico solicitado
    Soporta: bar, pie, line, donut, horizontalBar, bubble, scatter, gauge
    """
    query_lower = user_query.lower()
    
    # Donut (prioridad alta - más específico)
    if any(kw in query_lower for kw in ['donut', 'dona', 'rosquilla', 'anillo']):
        return 'donut'
    
    # Horizontal Bar
    elif any(kw in query_lower for kw in ['horizontal', 'barra horizontal', 'barras horizontales']):
        return 'horizontalBar'
    
    # Bubble/Scatter
    elif any(kw in query_lower for kw in ['burbuja', 'burbujas', 'bubble']):
        return 'bubble'
    elif any(kw in query_lower for kw in ['scatter', 'dispersión', 'dispersion', 'puntos']):
        return 'scatter'
    
    # Gauge/Radial
    elif any(kw in query_lower for kw in ['gauge', 'indicador', 'velocímetro', 'velocimetro', 'radial', 'medidor']):
        return 'gauge'
    
    # Tipos básicos (ya existentes)
    elif any(kw in query_lower for kw in ['barra', 'barras', 'bar']) and 'horizontal' not in query_lower:
        return 'bar'
    elif any(kw in query_lower for kw in ['torta', 'pie', 'circular', 'pastel']) and 'donut' not in query_lower:
        return 'pie'
    elif any(kw in query_lower for kw in ['línea', 'linea', 'line', 'tendencia']):
        return 'line'
    
    else:
        # Default según contexto de query
        if any(kw in query_lower for kw in ['evolución', 'evolucion', 'temporal', 'tiempo', 'mes', 'año']):
            return 'line'
        elif any(kw in query_lower for kw in ['distribución', 'distribucion', 'proporción', 'proporcion', 'share']):
            return 'donut'  # Donut es más moderno que pie para distribuciones
        else:
            return 'bar'  # Default


def generate_chart_metadata(query_type, data, user_query):
    """
    Genera título y descripción del gráfico basado en los datos
    Python analiza y genera estos metadatos (NO Claude)
    """
    
    if query_type == "ranking":
        num_clients = len(data)
        total_facturacion = sum(r.get('facturacion', 0) for r in data)
        
        title = f"Top {num_clients} Clientes por Facturación"
        description = f"Ranking de clientes ordenados por facturación total descendente. Total: {total_facturacion:,.0f} Gs"
        
    elif query_type == "facturacion":
        if data:
            cliente = data[0].get('cliente', 'Cliente')
            title = f"Facturación de {cliente}"
            description = f"Análisis de facturación total y promedio mensual"
        else:
            title = "Facturación de Cliente"
            description = "Análisis de facturación"
    
    elif query_type == "comparacion":
        if len(data) >= 2:
            title = f"Comparación de Clientes"
            description = f"Análisis comparativo entre {len(data)} clientes"
        else:
            title = "Comparación de Clientes"
            description = "Análisis comparativo"
    
    elif query_type == "market_share":
        title = "Distribución de Market Share"
        description = f"Participación de mercado de los principales {len(data)} clientes"
    
    else:
        # Genérico
        title = "Análisis de Facturación"
        description = f"Visualización de {len(data)} registros"
    
    return {
        "title": title,
        "description": description
    }


def build_chart_config(user_query, query_type, data):
    """
    Construye la configuración completa del gráfico
    Incluye: tipo, título, descripción, formato, y configs específicas
    """
    
    chart_type = detect_chart_type(user_query)
    metadata = generate_chart_metadata(query_type, data, user_query)
    
    config = {
        "type": chart_type,
        "title": metadata["title"],
        "description": metadata["description"],
        "format": {
            "currency": "Gs",
            "locale": "es-PY"
        }
    }
    
    # Configuraciones específicas según tipo de gráfico
    if chart_type == 'gauge':
        # Para gauge, necesitamos calcular un valor porcentual o de cumplimiento
        if data and len(data) > 0:
            total = sum(r.get('facturacion', 0) for r in data)
            # Calcular % del top cliente vs total
            top_cliente = data[0].get('facturacion', 0)
            percentage = (top_cliente / total * 100) if total > 0 else 0
            config['gauge_value'] = round(percentage, 1)
            config['gauge_label'] = f"{data[0].get('cliente', 'Cliente')} representa"
    
    elif chart_type == 'bubble' or chart_type == 'scatter':
        # Para bubble/scatter, necesitamos datos con x, y, y opcionalmente z (tamaño)
        # Preparar datos si es necesario
        config['scatter_config'] = {
            'x_label': 'Facturación',
            'y_label': 'Market Share',
            'z_label': 'Tamaño'
        }
    
    logger.info(f"📊 Gráfico configurado: {chart_type} - {metadata['title']}")
    
    return config


def should_include_chart(user_query):
    """
    Determina si la query requiere un gráfico
    Más específico que la versión anterior
    """
    intent = detect_query_intent(user_query)
    return intent in ["chart_only", "chart_and_text"]


def should_include_text(user_query):
    """
    Determina si la query requiere análisis de texto
    """
    intent = detect_query_intent(user_query)
    return intent in ["text_only", "chart_and_text"]


def build_table_config(query_type, data, user_query):
    """
    Construye configuración para tabla de datos
    """
    metadata = generate_chart_metadata(query_type, data, user_query)
    
    # Detectar columnas automáticamente desde los datos
    columns = []
    if data and len(data) > 0:
        first_row = data[0]
        
        # Mapeo de nombres técnicos a nombres amigables
        column_labels = {
            'cliente': 'Cliente',
            'facturacion': 'Facturación (Gs)',
            'market_share': 'Market Share (%)',
            'promedio_mensual': 'Promedio Mensual (Gs)',
            'registros': 'Registros'
        }
        
        for key in first_row.keys():
            columns.append({
                'key': key,
                'label': column_labels.get(key, key.replace('_', ' ').title()),
                'type': 'currency' if 'facturacion' in key else 'percentage' if 'share' in key else 'text'
            })
    
    config = {
        "type": "table",
        "title": metadata["title"],
        "description": metadata["description"],
        "columns": columns,
        "show_totals": True,
        "sortable": True,
        "format": {
            "currency": "Gs",
            "locale": "es-PY"
        }
    }
    
    logger.info(f"📋 Tabla configurada: {len(columns)} columnas, {len(data)} filas")
    
    return config


def build_kpi_config(query_type, data, user_query):
    """
    Construye configuración para cuadro de KPIs/métricas
    """
    metadata = generate_chart_metadata(query_type, data, user_query)
    
    kpis = []
    
    if query_type == "ranking" and data:
        # KPIs para ranking
        total = sum(r.get('facturacion', 0) for r in data)
        num_clients = len(data)
        top_cliente = data[0] if data else {}
        
        kpis = [
            {
                "label": "Total Facturación",
                "value": total,
                "format": "currency",
                "trend": None
            },
            {
                "label": "Clientes Analizados",
                "value": num_clients,
                "format": "number",
                "trend": None
            },
            {
                "label": "Líder del Ranking",
                "value": top_cliente.get('cliente', 'N/A'),
                "format": "text",
                "trend": None
            },
            {
                "label": "Market Share Líder",
                "value": top_cliente.get('market_share', 0),
                "format": "percentage",
                "trend": "up" if top_cliente.get('market_share', 0) > 10 else "neutral"
            }
        ]
    
    elif query_type == "facturacion" and data:
        # KPIs para facturación específica
        cliente = data[0] if data else {}
        
        kpis = [
            {
                "label": "Facturación Total",
                "value": cliente.get('facturacion', 0),
                "format": "currency",
                "trend": None
            },
            {
                "label": "Promedio Mensual",
                "value": cliente.get('promedio_mensual', 0),
                "format": "currency",
                "trend": None
            },
            {
                "label": "Market Share",
                "value": cliente.get('market_share', 0),
                "format": "percentage",
                "trend": None
            },
            {
                "label": "Registros",
                "value": cliente.get('registros', 0),
                "format": "number",
                "trend": None
            }
        ]
    
    config = {
        "type": "kpi",
        "title": metadata["title"],
        "description": metadata["description"],
        "kpis": kpis,
        "format": {
            "currency": "Gs",
            "locale": "es-PY"
        }
    }
    
    logger.info(f"📊 KPI Card configurado: {len(kpis)} métricas")
    
    return config