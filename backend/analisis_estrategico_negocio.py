"""
ANÁLISIS ESTRATÉGICO DE NEGOCIO
Respuestas a consultas específicas con datos cruzados
"""

from app import engine
from sqlalchemy import text
import json

def analizar_alex_sa():
    """
    1. Alex S.A. - ¿Capturamos su importancia o se escapan servicios digitales?
    """
    
    print("🔍 ANÁLISIS: ALEX S.A.")
    print("="*50)
    
    try:
        with engine.connect() as conn:
            # Datos completos Alex
            stmt = text("""
                SELECT 
                    p.nombre_anunciante,
                    CAST(p.inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT) as inversion_tv_usd,
                    p.cluster,
                    p.competitividad,
                    p.la_empresa_invierte_en_digital,
                    COALESCE(SUM(f.facturacion), 0) as facturacion_total,
                    COALESCE(SUM(f.revenue), 0) as revenue_total,
                    COUNT(f.*) as registros,
                    STRING_AGG(DISTINCT f.division, ', ') as divisiones,
                    STRING_AGG(DISTINCT f.arena, ', ') as arenas
                FROM dim_anunciante_perfil p
                LEFT JOIN fact_facturacion f ON p.anunciante_id = f.anunciante_id
                WHERE p.nombre_anunciante = 'ALEX'
                GROUP BY p.nombre_anunciante, p.inversion_en_tv_abierta_2024_en_miles_usd, 
                         p.cluster, p.competitividad, p.la_empresa_invierte_en_digital
            """)
            
            result = conn.execute(stmt).fetchone()
            
            if result:
                inversion_tv = result.inversion_tv_usd or 0
                facturacion = result.facturacion_total or 0
                revenue = result.revenue_total or 0
                digital_score = result.la_empresa_invierte_en_digital or 0
                
                print(f"📺 Inversión TV AdLens: ${inversion_tv:,.0f} USD")
                print(f"💰 Facturación con nosotros: {facturacion:,.0f} Gs")
                print(f"💰 Revenue generado: {revenue:,.0f} Gs") 
                print(f"🎯 Digital score: {digital_score}/10")
                print(f"📊 Registros: {result.registros}")
                print(f"🏢 Divisiones: {result.divisiones}")
                print(f"🎪 Arenas: {result.arenas}")
                
                # Cálculo ratio
                if inversion_tv > 0 and facturacion > 0:
                    # Convertir facturación a USD aproximado (1 USD = 7500 Gs aprox)
                    facturacion_usd = facturacion / 7500
                    ratio = facturacion_usd / inversion_tv * 100
                    
                    print(f"\n🎯 ANÁLISIS ESTRATÉGICO:")
                    print(f"   Facturación USD aprox: ${facturacion_usd:,.0f}")
                    print(f"   Ratio captura: {ratio:.1f}% de su inversión TV")
                    
                    if ratio < 10:
                        print("   ⚠️  OPORTUNIDAD: Muy baja captura vs inversión")
                        print("   💡 Recomendación: Explorar servicios digitales")
                    elif ratio < 25:
                        print("   ⚡ Captura moderada - potencial de crecimiento")
                    else:
                        print("   ✅ Buena captura de su inversión")
                else:
                    print(f"\n❌ Sin facturación registrada - GRAN OPORTUNIDAD")
            else:
                print("❌ Alex S.A. no encontrado")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def analizar_puma_energy():
    """
    2. Puma Energy - ¿Se nota su perfil innovador en nuestros servicios?
    """
    
    print("\n🔍 ANÁLISIS: PUMA ENERGY")
    print("="*50)
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    p.nombre_anunciante,
                    p.cluster,
                    p.cultura,
                    p.competitividad,
                    p.la_empresa_invierte_en_digital,
                    COALESCE(SUM(f.facturacion), 0) as facturacion_total,
                    STRING_AGG(DISTINCT f.division, ', ') as divisiones,
                    STRING_AGG(DISTINCT f.arena, ', ') as arenas
                FROM dim_anunciante_perfil p
                LEFT JOIN fact_facturacion f ON p.anunciante_id = f.anunciante_id
                WHERE p.nombre_anunciante LIKE '%PUMA%'
                GROUP BY p.nombre_anunciante, p.cluster, p.cultura, p.competitividad, p.la_empresa_invierte_en_digital
            """)
            
            result = conn.execute(stmt).fetchone()
            
            if result:
                print(f"🎯 Cluster: {result.cluster}")
                print(f"🎨 Cultura: {result.cultura}")
                print(f"⚡ Competitividad: {result.competitividad}")
                print(f"💻 Digital score: {result.la_empresa_invierte_en_digital}/10")
                print(f"💰 Facturación: {result.facturacion_total:,.0f} Gs")
                print(f"🏢 Divisiones: {result.divisiones}")
                print(f"🎪 Arenas: {result.arenas}")
                
                print(f"\n🎯 ANÁLISIS DE INNOVACIÓN:")
                
                # Evaluar si les hacemos servicios innovadores
                arenas = result.arenas or ""
                divisiones = result.divisiones or ""
                
                servicios_innovadores = 0
                servicios_tradicionales = 0
                
                if "CREACION" in arenas.upper():
                    servicios_innovadores += 1
                if "BI" in arenas.upper():
                    servicios_innovadores += 1
                if "DISTRIBUCION" in arenas.upper():
                    servicios_tradicionales += 1
                if "FEE FIJO" in divisiones.upper():
                    servicios_tradicionales += 1
                
                if servicios_innovadores > servicios_tradicionales:
                    print("   ✅ Les prestamos servicios INNOVADORES")
                elif servicios_innovadores == servicios_tradicionales:
                    print("   ⚡ Mix balanceado - potencial para más innovación")
                else:
                    print("   ⚠️  OPORTUNIDAD: Más servicios tradicionales que innovadores")
                    print("   💡 Recomendación: Ofrecer más creación y BI")
            else:
                print("❌ Puma Energy no encontrado")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def analizar_empresas_innovadoras():
    """
    5. ¿Qué empresas se destacan por Innovar en Publicidad?
    """
    
    print("\n🔍 ANÁLISIS: EMPRESAS INNOVADORAS")
    print("="*50)
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    p.nombre_anunciante,
                    CAST(p.competitividad AS FLOAT) as competitividad,
                    CAST(p.la_empresa_invierte_en_digital AS FLOAT) as digital_score,
                    p.cluster,
                    COALESCE(SUM(f.facturacion), 0) as facturacion_total,
                    STRING_AGG(DISTINCT f.arena, ', ') as arenas
                FROM dim_anunciante_perfil p
                LEFT JOIN fact_facturacion f ON p.anunciante_id = f.anunciante_id
                WHERE p.competitividad != '-' AND p.competitividad IS NOT NULL
                  AND p.la_empresa_invierte_en_digital != '-' AND p.la_empresa_invierte_en_digital IS NOT NULL
                  AND CAST(p.competitividad AS FLOAT) >= 0.8
                  AND CAST(p.la_empresa_invierte_en_digital AS FLOAT) >= 8
                GROUP BY p.nombre_anunciante, p.competitividad, p.la_empresa_invierte_en_digital, p.cluster
                HAVING SUM(f.facturacion) > 0
                ORDER BY CAST(p.competitividad AS FLOAT) DESC, CAST(p.la_empresa_invierte_en_digital AS FLOAT) DESC
                LIMIT 10
            """)
            
            results = conn.execute(stmt).fetchall()
            
            print("🏆 TOP EMPRESAS INNOVADORAS:")
            print("   (Competitividad ≥ 0.8 + Digital ≥ 8)")
            print()
            
            for i, row in enumerate(results, 1):
                arenas = row.arenas or "Sin datos"
                print(f"{i:2d}. {row.nombre_anunciante}")
                print(f"    Competitividad: {row.competitividad:.1f}")
                print(f"    Digital: {row.digital_score:.0f}/10")
                print(f"    Cluster: {row.cluster}")
                print(f"    Facturación: {row.facturacion_total:,.0f} Gs")
                print(f"    Servicios: {arenas}")
                print()
    
    except Exception as e:
        print(f"❌ Error: {e}")

def analizar_depto_marketing_vs_agencia():
    """
    6. ¿Se crece más con Departamento de Marketing o con Agencia?
    """
    
    print("\n🔍 ANÁLISIS: DEPTO MARKETING vs AGENCIA")
    print("="*50)
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    p.tiene_la_empresa_departamento_de_marketing as tiene_depto,
                    p.central_de_medios,
                    COUNT(*) as total_empresas,
                    AVG(COALESCE(f.facturacion, 0)) as facturacion_promedio,
                    SUM(COALESCE(f.facturacion, 0)) as facturacion_total,
                    AVG(CAST(
                        CASE WHEN p.competitividad = '-' OR p.competitividad IS NULL THEN NULL 
                             ELSE p.competitividad END AS FLOAT)) as competitividad_promedio
                FROM dim_anunciante_perfil p
                LEFT JOIN fact_facturacion f ON p.anunciante_id = f.anunciante_id
                WHERE p.tiene_la_empresa_departamento_de_marketing IS NOT NULL
                GROUP BY p.tiene_la_empresa_departamento_de_marketing, p.central_de_medios
                HAVING COUNT(*) > 5
                ORDER BY facturacion_promedio DESC
            """)
            
            results = conn.execute(stmt).fetchall()
            
            print("📊 FACTURACIÓN POR ESTRUCTURA:")
            print()
            
            for row in results:
                depto = row.tiene_depto or "Sin especificar"
                central = row.central_de_medios or "Sin central"
                
                print(f"🏢 {depto} + {central}")
                print(f"   Empresas: {row.total_empresas}")
                print(f"   Facturación promedio: {row.facturacion_promedio:,.0f} Gs")
                print(f"   Facturación total: {row.facturacion_total:,.0f} Gs")
                print(f"   Competitividad: {row.competitividad_promedio:.2f}")
                print()
    
    except Exception as e:
        print(f"❌ Error: {e}")

def analizar_cultura_vs_inversion():
    """
    7. Diferencia entre Cultura e Inversión
    """
    
    print("\n🔍 ANÁLISIS: CULTURA vs INVERSIÓN")
    print("="*50)
    
    try:
        with engine.connect() as conn:
            stmt = text("""
                SELECT 
                    CASE 
                        WHEN CAST(p.cultura AS FLOAT) >= 0.8 THEN 'Alta Cultura (≥0.8)'
                        WHEN CAST(p.cultura AS FLOAT) >= 0.5 THEN 'Media Cultura (0.5-0.7)'
                        ELSE 'Baja Cultura (<0.5)'
                    END as nivel_cultura,
                    COUNT(*) as empresas,
                    AVG(CAST(p.inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT)) as inversion_tv_promedio,
                    AVG(CAST(p.la_empresa_invierte_en_digital AS FLOAT)) as digital_promedio,
                    AVG(COALESCE(f.facturacion, 0)) as facturacion_promedio
                FROM dim_anunciante_perfil p
                LEFT JOIN fact_facturacion f ON p.anunciante_id = f.anunciante_id
                WHERE p.cultura != '-' AND p.cultura IS NOT NULL
                  AND p.inversion_en_tv_abierta_2024_en_miles_usd != '-' 
                  AND p.la_empresa_invierte_en_digital != '-'
                GROUP BY CASE 
                        WHEN CAST(p.cultura AS FLOAT) >= 0.8 THEN 'Alta Cultura (≥0.8)'
                        WHEN CAST(p.cultura AS FLOAT) >= 0.5 THEN 'Media Cultura (0.5-0.7)'
                        ELSE 'Baja Cultura (<0.5)'
                    END
                ORDER BY AVG(CAST(p.cultura AS FLOAT)) DESC
            """)
            
            results = conn.execute(stmt).fetchall()
            
            print("🎨 CORRELACIÓN CULTURA-INVERSIÓN:")
            print()
            
            for row in results:
                print(f"📊 {row.nivel_cultura}")
                print(f"   Empresas: {row.empresas}")
                print(f"   Inversión TV promedio: ${row.inversion_tv_promedio:,.0f} USD")
                print(f"   Score digital promedio: {row.digital_promedio:.1f}/10")
                print(f"   Facturación promedio: {row.facturacion_promedio:,.0f} Gs")
                print()
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 ANÁLISIS ESTRATÉGICO DE NEGOCIO")
    print("="*70)
    print("Respondiendo preguntas específicas con datos cruzados")
    print()
    
    # Ejecutar todos los análisis
    analizar_alex_sa()
    analizar_puma_energy()
    analizar_empresas_innovadoras()
    analizar_depto_marketing_vs_agencia()
    analizar_cultura_vs_inversion()
    
    print("🎉 ANÁLISIS COMPLETADO")
    print("Insights estratégicos basados en datos reales")

