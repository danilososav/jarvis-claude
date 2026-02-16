"""
FIX: Error análisis clusters - valores "-" en campos numéricos
"""

def consulta_analisis_clusters_fixed(user_query, db_engine):
    """
    Análisis por clusters con manejo de valores "-"
    """
    
    logger.info(f"🔍 Análisis clusters (fixed): {user_query}")
    
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
                            WHEN p.competitividad = '-' OR p.competitividad IS NULL THEN NULL
                            ELSE CAST(p.competitividad AS FLOAT)
                        END
                    ) as competitividad_promedio,
                    AVG(
                        CASE 
                            WHEN p.puntaje_total = '-' OR p.puntaje_total IS NULL THEN NULL
                            ELSE CAST(p.puntaje_total AS FLOAT)
                        END
                    ) as puntaje_promedio,
                    SUM(
                        CASE 
                            WHEN p.inversion_en_tv_abierta_2024_en_miles_usd = '-' OR p.inversion_en_tv_abierta_2024_en_miles_usd IS NULL THEN 0
                            ELSE CAST(p.inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT)
                        END
                    ) as inversion_tv_total,
                    SUM(
                        CASE 
                            WHEN p.inversion_en_radio_2024_en_miles_usd = '-' OR p.inversion_en_radio_2024_en_miles_usd IS NULL THEN 0
                            ELSE CAST(p.inversion_en_radio_2024_en_miles_usd AS FLOAT)
                        END
                    ) as inversion_radio_total,
                    SUM(
                        CASE 
                            WHEN p.inversion_en_cable_2024_en_miles_usd = '-' OR p.inversion_en_cable_2024_en_miles_usd IS NULL THEN 0
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
        logger.error(f"❌ Error análisis clusters fixed: {e}")
        return {'error': str(e)}

# REEMPLAZAR EN consultas_complejas_sin_claude.py
# La función consulta_analisis_clusters() por esta versión fixed

if __name__ == "__main__":
    print("🔧 FIX: Análisis por clusters")
    print("✅ Maneja valores '-' en campos numéricos")
    print("✅ Usa CASE WHEN para validar antes de CAST")
    print("✅ Convierte '-' a NULL o 0 según corresponda")

