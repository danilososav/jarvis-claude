"""
VERIFICACIÓN DIRECTA SIN CLAUDE
Comprueba que los números coincidan exactamente con Excel
"""

from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:123@localhost/jarvis")

def verificar_sin_claude():
    """Verificación directa de los números"""
    
    print("🔍 VERIFICACIÓN DIRECTA BD vs EXCEL")
    print("=" * 50)
    
    with engine.connect() as conn:
        # LA CONSULTA EXACTA QUE DEBERÍA USAR JARVIS CORREGIDA
        stmt = text("""
            SELECT 
                f.cliente_original,
                SUM(f.facturacion)::float as facturacion,
                COUNT(*) as registros
            FROM fact_facturacion f
            WHERE f.facturacion > 0 
                AND f.anio = 2025
                AND f.cliente_original IS NOT NULL
            GROUP BY f.cliente_original
            ORDER BY facturacion DESC
            LIMIT 10
        """)
        
        result = conn.execute(stmt).fetchall()
        
        print("🏆 TOP 10 DE LA BD (después de corrección):")
        print("-" * 70)
        
        for i, row in enumerate(result, 1):
            print(f"{i:2d}. {row.cliente_original[:45]:<45} {row.registros:>5} reg {row.facturacion:>15,.0f} Gs")
        
        print()
        print("🎯 NÚMEROS ESPERADOS DEL EXCEL:")
        print("-" * 70)
        print(" 1. CERVEPAR S.A.                                  1136 reg  26,057,164,652 Gs")
        print(" 2. TELEFONICA CELULAR DEL PARAGUAY S.A.E.          186 reg   9,213,656,412 Gs")
        print(" 3. ALEX S.A.                                      1046 reg   7,648,184,682 Gs")
        print(" 4. CEAMSO                                           30 reg   7,143,491,271 Gs")
        print(" 5. BANCO FAMILIAR S.A.E.C.A.                       377 reg   7,043,783,797 Gs")
        
        print()
        
        # Verificar específicos
        cervepar = next((r for r in result if 'CERVEPAR' in r.cliente_original), None)
        telefonica = next((r for r in result if 'TELEFONICA' in r.cliente_original), None)
        
        if cervepar:
            cervepar_correcto = abs(cervepar.facturacion - 26057164652) < 1000
            print(f"✅ CERVEPAR: {cervepar.facturacion:,.0f} Gs {'✅ CORRECTO' if cervepar_correcto else '❌ INCORRECTO'}")
        
        if telefonica:
            telefonica_correcto = abs(telefonica.facturacion - 9213656412) < 1000  
            print(f"✅ TELEFÓNICA: {telefonica.facturacion:,.0f} Gs {'✅ CORRECTO' if telefonica_correcto else '❌ INCORRECTO'}")
        
        if cervepar and telefonica and cervepar_correcto and telefonica_correcto:
            print()
            print("🎉 ¡NÚMEROS CORRECTOS!")
            print("✅ La corrección funcionó")
            print("✅ JARVIS ahora será exacto")
        else:
            print()
            print("❌ Los números aún no coinciden")
            print("❌ Verificar que los 3 cambios se hicieron correctamente")

if __name__ == "__main__":
    verificar_sin_claude()
