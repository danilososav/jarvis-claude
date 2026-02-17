"""
Test directo de la función get_top_clientes_enriched
"""

from sqlalchemy import create_engine, text
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conectar BD
engine = create_engine("postgresql://postgres:123@localhost/jarvis")

def test_get_top_clientes_enriched():
    """Test de la función corregida"""
    try:
        with engine.connect() as conn:
            # LA CONSULTA EXACTA QUE DEBERÍA ESTAR EN app.py
            stmt = text("""
                SELECT 
                    d.nombre_canonico,
                    SUM(f.facturacion)::float as facturacion,
                    COUNT(*) as registros,
                    (SUM(f.facturacion) / NULLIF((SELECT SUM(facturacion) FROM fact_facturacion WHERE facturacion > 0 AND anio = 2025), 0) * 100)::float as market_share
                FROM dim_anunciante d
                LEFT JOIN fact_facturacion f ON d.anunciante_id = f.anunciante_id
                WHERE f.facturacion > 0 AND f.anio = 2025
                GROUP BY d.anunciante_id, d.nombre_canonico
                HAVING SUM(f.facturacion) > 0
                ORDER BY facturacion DESC
                LIMIT 5
            """)
            
            rows = conn.execute(stmt).fetchall()
            
            print("🔍 TEST DE FUNCIÓN CORREGIDA:")
            print("=" * 50)
            
            result = []
            for i, r in enumerate(rows, 1):
                cliente = r[0] or "Sin nombre"
                facturacion = float(r[1]) if r[1] else 0
                registros = int(r[2]) if r[2] else 0
                market_share = float(r[3]) if r[3] else 0
                
                print(f"{i}. {cliente}")
                print(f"   Facturación: {facturacion:,.0f} Gs")
                print(f"   Registros: {registros}")
                print(f"   Market Share: {market_share:.2f}%")
                print()
                
                result.append({
                    "cliente": cliente,
                    "facturacion": facturacion,
                    "registros": registros,
                    "market_share": market_share
                })
            
            print("🎯 NÚMEROS ESPERADOS vs OBTENIDOS:")
            print("CERVEPAR debería ser: 26,057,164,652 Gs")
            print("TELEFÓNICA debería ser: 9,213,656,412 Gs")
            
            return result
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return []

if __name__ == "__main__":
    test_get_top_clientes_enriched()
