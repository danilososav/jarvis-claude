"""
EXPANSIÓN format_data_for_claude PARA DATOS 360°
Maneja estructura completa: ERP + AdLens + DNIT integrados
"""

def format_data_for_claude_360(rows, query_type):
    """
    ✅ VERSIÓN 360° - Formatea datos completos para Claude
    Reemplaza la función original para manejar estructura integrada
    """
    
    if not rows:
        return []
    
    # Procesar cada cliente en la respuesta
    formatted_clients = []
    
    for row in rows:
        # CLIENTE 360° - Estructura completa
        cliente_360 = {
            # IDENTIFICACIÓN BÁSICA
            'cliente': row.get('cliente', 'N/A'),
            'anunciante_id': row.get('anunciante_id'),
            
            # FACTURACIÓN ERP COMPLETA
            'facturacion': row.get('facturacion', 0),
            'revenue': row.get('revenue', 0),
            'costo': row.get('costo', 0),
            'promedio_mensual': row.get('promedio_mensual', 0),
            'registros': row.get('registros', 0),
            'divisiones': row.get('divisiones', ''),
            'arenas': row.get('arenas', ''),
            
            # POSICIONAMIENTO DNIT
            'ranking': row.get('ranking'),
            'aporte_dnit': row.get('aporte_dnit', 0),
            'ingreso_estimado': row.get('ingreso_estimado', 0),
            
            # PERFIL ADLENS ESTRATÉGICO
            'rubro': row.get('rubro', ''),
            'tamano_empresa': row.get('tamano_empresa', ''),
            'cluster': row.get('cluster', ''),
            'tipo_cluster': row.get('tipo_cluster', ''),
            'cultura': row.get('cultura', ''),
            'ejecucion': row.get('ejecucion', ''),
            'estructura': row.get('estructura', ''),
            'competitividad': row.get('competitividad', 0),
            'puntaje_total': row.get('puntaje_total', 0),
            
            # INVERSIONES COMPLETAS (6 MEDIOS)
            'inversion_total_usd': row.get('inversion_total_usd', 0),
            'inversiones_detalle': row.get('inversiones_detalle', {}),
            'mix_medios': row.get('mix_medios', {}),
            
            # KPIS CALCULADOS
            'roi_publicitario': row.get('roi_publicitario', 0),
            'market_share': row.get('market_share', 0),
            'nivel_inversion': row.get('nivel_inversion', 'Sin datos'),
            'perfil_estrategico': row.get('perfil_estrategico', ''),
            
            # ORGANIZACIONAL
            'central_medios': row.get('central_medios', ''),
            'tiene_marketing': row.get('tiene_marketing', ''),
            'medios_principales': row.get('medios_principales', ''),
            'invierte_digital': row.get('invierte_digital', ''),
            
            # EVOLUCIÓN TEMPORAL
            'evolucion_mensual': row.get('evolucion_mensual', [])
        }
        
        formatted_clients.append(cliente_360)
    
    return formatted_clients

def expand_claude_handler_360():
    """
    EXPANSIÓN del claude_handler_v2.py para análisis 360°
    """
    
    new_format_data_method = '''
def _format_data(self, data: List[Dict], query_type: str) -> str:
    """
    ✅ VERSIÓN 360° - Formatea datos completos para prompt de Claude
    """
    if not data:
        return "No hay datos disponibles"
    
    if query_type == "ranking":
        return self._format_ranking_360(data)
    elif query_type == "facturacion":
        return self._format_cliente_360(data[0])
    elif query_type == "comparacion":
        return self._format_comparacion_360(data)
    elif query_type == "perfil_completo":
        return self._format_perfil_estrategico_360(data[0])
    else:
        return self._format_generico_360(data)

def _format_cliente_360(self, cliente: Dict) -> str:
    """
    Formato 360° para un cliente individual
    """
    
    # DATOS BASE
    result = f"""CLIENTE: {cliente.get('cliente', 'N/A')}
IDENTIFICACIÓN:
• Rubro: {cliente.get('rubro', 'N/A')}
• Tamaño: {cliente.get('tamano_empresa', 'N/A')}

PERFORMANCE FINANCIERO:
• Facturación Total: {cliente.get('facturacion', 0):,.0f} Gs
• Revenue: {cliente.get('revenue', 0):,.0f} Gs
• Promedio Mensual: {cliente.get('promedio_mensual', 0):,.0f} Gs
• Divisiones: {cliente.get('divisiones', 'N/A')}
• Arenas: {cliente.get('arenas', 'N/A')}"""
    
    # POSICIONAMIENTO DNIT
    if cliente.get('ranking'):
        result += f"""

POSICIONAMIENTO DNIT:
• Ranking: #{cliente.get('ranking')}
• Aporte DNIT: {cliente.get('aporte_dnit', 0):,.0f} Gs
• Ingreso Estimado: {cliente.get('ingreso_estimado', 0):,.0f} Gs"""
    
    # PERFIL ESTRATÉGICO ADLENS
    if cliente.get('cluster'):
        result += f"""

PERFIL ESTRATÉGICO:
• Cluster: {cliente.get('cluster')} ({cliente.get('tipo_cluster', '')})
• Cultura: {cliente.get('cultura', 'N/A')}
• Ejecución: {cliente.get('ejecucion', 'N/A')}
• Estructura: {cliente.get('estructura', 'N/A')}
• Competitividad: {cliente.get('competitividad', 0)}/10
• Puntaje Total: {cliente.get('puntaje_total', 0)}/100"""
    
    # INVERSIONES 360° (TODOS LOS MEDIOS)
    if cliente.get('inversion_total_usd', 0) > 0:
        result += f"""

INVERSIÓN PUBLICITARIA 2024:
• Total: ${cliente.get('inversion_total_usd', 0):,.0f} USD
• ROI: {cliente.get('roi_publicitario', 0):.2f}% vs facturación
• Nivel: {cliente.get('nivel_inversion', 'N/A')}

DISTRIBUCIÓN POR MEDIO:"""
        
        # Detallar cada medio
        mix_medios = cliente.get('mix_medios', {})
        for medio, datos in mix_medios.items():
            if datos.get('monto_usd', 0) > 0:
                result += f"""
• {medio}: ${datos.get('monto_usd', 0):,.0f} USD ({datos.get('porcentaje', 0):.1f}%)"""
    else:
        result += f"""

INVERSIÓN PUBLICITARIA:
• Sin datos de inversión registrados en 2024"""
    
    # ORGANIZACIONAL
    if cliente.get('central_medios') or cliente.get('tiene_marketing'):
        result += f"""

ORGANIZACIÓN:
• Central de Medios: {cliente.get('central_medios', 'N/A')}
• Departamento Marketing: {cliente.get('tiene_marketing', 'N/A')}
• Medios Principales: {cliente.get('medios_principales', 'N/A')}
• Invierte Digital: {cliente.get('invierte_digital', 'N/A')}"""
    
    # KPIS CALCULADOS
    if cliente.get('market_share', 0) > 0:
        result += f"""

MARKET PERFORMANCE:
• Market Share: {cliente.get('market_share', 0):.2f}%
• Perfil Estratégico: {cliente.get('perfil_estrategico', 'N/A')}"""
    
    return result

def _format_perfil_estrategico_360(self, cliente: Dict) -> str:
    """
    Formato especializado para análisis de perfil estratégico completo
    """
    
    return f"""ANÁLISIS ESTRATÉGICO 360°: {cliente.get('cliente', 'N/A')}

═══ IDENTIFICACIÓN EMPRESARIAL ═══
• Rubro: {cliente.get('rubro', 'N/A')}
• Tamaño: {cliente.get('tamano_empresa', 'N/A')}
• Posición DNIT: #{cliente.get('ranking', 'N/A')} 

═══ PERFIL ADLENS COMPLETO ═══
• Cluster: {cliente.get('cluster', 'N/A')} - {cliente.get('tipo_cluster', '')}
• Cultura Organizacional: {cliente.get('cultura', 'N/A')}
• Ejecución: {cliente.get('ejecucion', 'N/A')}
• Estructura: {cliente.get('estructura', 'N/A')}
• Score Competitividad: {cliente.get('competitividad', 0)}/10
• Puntaje Global: {cliente.get('puntaje_total', 0)}/100

═══ PERFORMANCE FINANCIERO ═══
• Facturación: {cliente.get('facturacion', 0):,.0f} Gs
• Market Share: {cliente.get('market_share', 0):.2f}%
• Aporte Sector: {cliente.get('aporte_dnit', 0):,.0f} Gs

═══ ESTRATEGIA DE MEDIOS ═══
• Inversión Total: ${cliente.get('inversion_total_usd', 0):,.0f} USD
• ROI Publicitario: {cliente.get('roi_publicitario', 0):.2f}%
• Distribución Cross-Media:""" + "".join([f"""
  - {medio}: ${datos.get('monto_usd', 0):,.0f} ({datos.get('porcentaje', 0):.1f}%)""" 
  for medio, datos in cliente.get('mix_medios', {}).items() 
  if datos.get('monto_usd', 0) > 0]) + f"""

═══ CAPACIDADES ORGANIZACIONALES ═══
• Central de Medios: {cliente.get('central_medios', 'N/A')}
• Departamento Marketing: {cliente.get('tiene_marketing', 'N/A')}
• Transformación Digital: {cliente.get('invierte_digital', 'N/A')}
• Medios Preferidos: {cliente.get('medios_principales', 'N/A')}"""

def _format_comparacion_360(self, clientes: List[Dict]) -> str:
    """
    Formato para comparaciones 360° entre múltiples clientes
    """
    
    if len(clientes) < 2:
        return "Se necesitan al menos 2 clientes para comparación"
    
    c1, c2 = clientes[0], clientes[1]
    
    return f"""COMPARACIÓN ESTRATÉGICA 360°

═══ CLIENTE A: {c1.get('cliente', 'N/A')} ═══
• Cluster: {c1.get('cluster', 'N/A')} | Cultura: {c1.get('cultura', 'N/A')}
• Facturación: {c1.get('facturacion', 0):,.0f} Gs
• Ranking DNIT: #{c1.get('ranking', 'N/A')}
• Inversión: ${c1.get('inversion_total_usd', 0):,.0f} USD (ROI: {c1.get('roi_publicitario', 0):.2f}%)
• Competitividad: {c1.get('competitividad', 0)}/10

═══ CLIENTE B: {c2.get('cliente', 'N/A')} ═══
• Cluster: {c2.get('cluster', 'N/A')} | Cultura: {c2.get('cultura', 'N/A')}
• Facturación: {c2.get('facturacion', 0):,.0f} Gs  
• Ranking DNIT: #{c2.get('ranking', 'N/A')}
• Inversión: ${c2.get('inversion_total_usd', 0):,.0f} USD (ROI: {c2.get('roi_publicitario', 0):.2f}%)
• Competitividad: {c2.get('competitividad', 0)}/10

═══ ANÁLISIS COMPARATIVO ═══
FACTURACIÓN:
• Diferencia: {abs(c1.get('facturacion', 0) - c2.get('facturacion', 0)):,.0f} Gs
• Líder: {c1.get('cliente') if c1.get('facturacion', 0) > c2.get('facturacion', 0) else c2.get('cliente')}

INVERSIÓN PUBLICITARIA:
• A - Mix principal: """ + ", ".join([f"{medio} ({datos.get('porcentaje', 0):.1f}%)" 
for medio, datos in c1.get('mix_medios', {}).items() 
if datos.get('porcentaje', 0) > 10])[:3] + f"""
• B - Mix principal: """ + ", ".join([f"{medio} ({datos.get('porcentaje', 0):.1f}%)" 
for medio, datos in c2.get('mix_medios', {}).items() 
if datos.get('porcentaje', 0) > 10])[:3] + f"""

PERFILES ESTRATÉGICOS:
• A: {c1.get('perfil_estrategico', 'N/A')}
• B: {c2.get('perfil_estrategico', 'N/A')}"""

def _format_ranking_360(self, clientes: List[Dict]) -> str:
    """
    Formato para rankings con datos 360°
    """
    
    result = "RANKING INTEGRADO - TOP ANUNCIANTES\n" + "="*50
    
    for i, cliente in enumerate(clientes, 1):
        facturacion = cliente.get('facturacion', 0)
        inversion = cliente.get('inversion_total_usd', 0)
        cluster = cliente.get('cluster', 'N/A')
        ranking_dnit = cliente.get('ranking')
        
        result += f"""

{i}. {cliente.get('cliente', 'N/A')}
   • Facturación: {facturacion:,.0f} Gs"""
        
        if ranking_dnit:
            result += f" | DNIT: #{ranking_dnit}"
            
        if cluster != 'N/A':
            result += f" | Cluster: {cluster}"
            
        if inversion > 0:
            result += f"""
   • Inversión: ${inversion:,.0f} USD ({cliente.get('roi_publicitario', 0):.2f}% ROI)"""
            
        result += f"""
   • Competitividad: {cliente.get('competitividad', 0)}/10"""
    
    return result
    '''
    
    print("🔧 NUEVA VERSIÓN CLAUDE HANDLER 360°:")
    print("="*50)
    print("✅ _format_cliente_360() - Análisis individual completo")
    print("✅ _format_perfil_estrategico_360() - Perfil estratégico profundo") 
    print("✅ _format_comparacion_360() - Comparaciones cross-empresa")
    print("✅ _format_ranking_360() - Rankings integrados")
    print("\n💬 PROMPTS RESULTANTES PARA CLAUDE:")
    print("-" * 40)
    print("• 6 tipos de medios (no solo TV)")
    print("• Clusters + cultura + ejecución")
    print("• ROI publicitario calculado")
    print("• Rankings DNIT integrados")
    print("• Performance organizacional")
    print("• Comparaciones estratégicas")
    
    return new_format_data_method

if __name__ == "__main__":
    print("🚀 EXPANSIÓN CLAUDE HANDLER 360°")
    print("="*60)
    
    # Mostrar nueva versión del format_data
    new_method = expand_claude_handler_360()
    
    print(f"\n📋 CÓDIGO PARA REEMPLAZAR EN claude_handler_v2.py:")
    print("-" * 60)
    print(new_method[:500] + "...")
    
    print(f"\n🎯 RESULTADO ESPERADO:")
    print("="*30)
    print("Claude ahora recibirá prompts como:")
    print('''
CLIENTE: UNILEVER DE PARAGUAY S.A.
PERFIL ESTRATÉGICO:
• Cluster: Consolidadas (Internacional)
• Cultura: Global | Ejecución: Diversificada
• Competitividad: 8.2/10

INVERSIÓN 2024: $139,000 USD (ROI: 1.7%)
• TV Abierta: $45,000 (32.4%)
• Radio: $32,000 (23.0%)
• Cable: $28,000 (20.1%)
...
    ''')

