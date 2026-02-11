"""
TEST DIAGNÓSTICO SIMPLE - CERVEZA DIOSA
Verificar datos reales en la BD
"""

from app import engine
from sqlalchemy import text
import logging

def test_cerveza_diosa_rapido():
    """
    Test rápido para diagnosticar CERVEZA DIOSA
    """
    
    print("🔍 TEST DIAGNÓSTICO: CERVEZA DIOSA (ID: 1577)")
    print("="*60)
    
    try:
        with engine.connect() as conn:
            
            # 1. ¿Existe en fact_facturacion?
            stmt = text("""
                SELECT 
                    COUNT(*) as registros,
                    SUM(facturacion) as total_facturacion,
                    SUM(revenue) as total_revenue,
                    MIN(fecha_fact) as primera_fecha,
                    MAX(fecha_fact) as ultima_fecha
                FROM fact_facturacion 
                WHERE anunciante_id = 1577
            """)
            
            result = conn.execute(stmt).fetchone()
            
            print("📊 FACT_FACTURACION:")
            print(f"   Registros: {result.registros}")
            print(f"   Facturación: {result.total_facturacion or 0:,.0f} Gs")
            print(f"   Revenue: {result.total_revenue or 0:,.0f} Gs")
            print(f"   Primera fecha: {result.primera_fecha}")
            print(f"   Última fecha: {result.ultima_fecha}")
            
            if result.registros == 0:
                print("   ⚠️ CERVEZA DIOSA NO ESTÁ EN fact_facturacion")
                print("   ✅ Es normal - no es cliente de facturación")
            
            # 2. ¿Qué datos tiene en AdLens?
            stmt = text("""
                SELECT 
                    nombre_anunciante,
                    cluster,
                    rubro_principal,
                    CAST(inversion_en_tv_abierta_2024_en_miles_usd AS FLOAT) as tv_usd,
                    CAST(inversion_en_radio_2024_en_miles_usd AS FLOAT) as radio_usd
                FROM dim_anunciante_perfil 
                WHERE anunciante_id = 1577
            """)
            
            result = conn.execute(stmt).fetchone()
            
            print(f"\n📊 DIM_ANUNCIANTE_PERFIL:")
            if result:
                print(f"   Nombre: {result.nombre_anunciante}")
                print(f"   Cluster: {result.cluster}")
                print(f"   Rubro: {result.rubro_principal}")
                print(f"   TV: ${result.tv_usd or 0} USD")
                print(f"   Radio: ${result.radio_usd or 0} USD")
            else:
                print("   ❌ No encontrado")
            
            # 3. ¿Está en ranking DNIT?
            stmt = text("""
                SELECT 
                    ranking,
                    aporte_gs,
                    razon_social
                FROM dim_posicionamiento_dnit 
                WHERE anunciante_id = 1577
            """)
            
            result = conn.execute(stmt).fetchone()
            
            print(f"\n📊 DIM_POSICIONAMIENTO_DNIT:")
            if result:
                print(f"   Ranking: #{result.ranking}")
                print(f"   Aporte: {result.aporte_gs:,.0f} Gs")
                print(f"   Razón social: {result.razon_social}")
            else:
                print("   ❌ No está en ranking DNIT")
            
            # 4. COMPARAR con un cliente que SÍ tiene datos
            print(f"\n📊 COMPARACIÓN CON CERVEPAR (ID: 3):")
            stmt = text("""
                SELECT 
                    COUNT(*) as registros,
                    SUM(facturacion) as total_facturacion
                FROM fact_facturacion 
                WHERE anunciante_id = 3
            """)
            
            result = conn.execute(stmt).fetchone()
            print(f"   CERVEPAR registros: {result.registros}")
            print(f"   CERVEPAR facturación: {result.total_facturacion or 0:,.0f} Gs")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🎯 CONCLUSIÓN:")
    print("Si CERVEZA DIOSA no está en fact_facturacion = NO es cliente de la agencia")
    print("Solo está en AdLens (datos del mercado) pero no factura con ustedes")
    print("= El sistema funciona CORRECTO, mostrando 0 porque realmente es 0")

if __name__ == "__main__":
    test_cerveza_diosa_rapido()

