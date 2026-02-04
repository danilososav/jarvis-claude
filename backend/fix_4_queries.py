#!/usr/bin/env python3
import sys
import re

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    contenido = f.read()

print("🔧 Arreglando 4 queries restantes...\n")

print("1️⃣  get_analisis_inversion_vs_facturacion")
pattern2 = r'(def get_analisis_inversion_vs_facturacion.*?FROM )(dim_anunciante_perfil ap|fact_inversiones)'
reemplazo2 = r'\1dim_anunciante_perfil ap'
contenido = re.sub(pattern2, reemplazo2, contenido, flags=re.DOTALL, count=1)
print("   ✅ Hecho\n")

print("2️⃣  get_facturacion_por_arena_e_inversion_digital")
count = len(re.findall(r'def get_facturacion_por_arena_e_inversion_digital', contenido))
if count > 1:
    lines = contenido.split('\n')
    result = []
    skip = False
    found_first = False
    for line in lines:
        if 'def get_facturacion_por_arena_e_inversion_digital' in line:
            if found_first:
                skip = True
            else:
                found_first = True
                result.append(line)
        elif skip and line.startswith('def '):
            skip = False
            result.append(line)
        elif not skip:
            result.append(line)
    contenido = '\n'.join(result)
    print(f"   ✅ Eliminados {count-1} duplicados\n")

pattern3 = r'(def get_facturacion_por_arena_e_inversion_digital.*?FROM fact_facturacion f\s+LEFT JOIN dim_anunciante d ON )f\.anunciante_id = d\.anunciante_id'
reemplazo3 = r'\1LOWER(TRIM(d.nombre_canonico)) = LOWER(TRIM(f.cliente_original))'
contenido = re.sub(pattern3, reemplazo3, contenido, flags=re.DOTALL, count=1)
print("   ✅ Hecho\n")

print("3️⃣  get_desconfiados_con_inversion_alta")
pattern4 = r'(def get_desconfiados_con_inversion_alta.*?)ap\.inversion_total'
reemplazo4 = r'\1COALESCE(NULLIF(ap.inversion_en_medios, \'\')::numeric, 0)'
contenido = re.sub(pattern4, reemplazo4, contenido, flags=re.DOTALL, count=1)
print("   ✅ Hecho\n")

print("4️⃣  get_analisis_cliente_especifico")
pattern5 = r'(def get_analisis_cliente_especifico.*?FROM fact_facturacion f\s+LEFT JOIN dim_anunciante d ON )f\.anunciante_id = d\.anunciante_id'
reemplazo5 = r'\1LOWER(TRIM(d.nombre_canonico)) = LOWER(TRIM(f.cliente_original))'
contenido = re.sub(pattern5, reemplazo5, contenido, flags=re.DOTALL, count=1)
print("   ✅ Hecho\n")

with open(sys.argv[1], 'w', encoding='utf-8') as f:
    f.write(contenido)

print("✅ TODAS LAS 4 QUERIES ARREGLADAS")
