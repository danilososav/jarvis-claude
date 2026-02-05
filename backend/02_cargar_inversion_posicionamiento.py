"""
Script de Carga: Inversión en Medios 2024 + Posicionamiento DNIT
Hace fuzzy matching con dim_anunciante para asignar anunciante_id
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from fuzzywuzzy import fuzz
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración BD
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'jarvis'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_anunciantes_existentes(conn):
    """Obtiene lista de anunciantes existentes (no usado con sistema de aliases)"""
    query = """
        SELECT 
            anunciante_id,
            nombre_canonico
        FROM dim_anunciante
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    
    anunciantes = []
    for row in rows:
        anunciante_id, nombre = row
        anunciantes.append({
            'id': anunciante_id,
            'nombre': nombre.upper() if nombre else ''
        })
    return anunciantes

def buscar_anunciante_por_nombre(conn, nombre):
    """
    Busca anunciante usando sistema de aliases
    1. Intenta búsqueda exacta con buscar_anunciante()
    2. Si no encuentra, usa fuzzy con threshold 80
    3. Si no encuentra, retorna None
    """
    cursor = conn.cursor()
    
    # Intento 1: Búsqueda exacta
    cursor.execute("SELECT buscar_anunciante(%s)", (nombre,))
    result = cursor.fetchone()
    
    if result and result[0]:
        cursor.close()
        return result[0], 100  # anunciante_id, confianza
    
    # Intento 2: Búsqueda fuzzy
    cursor.execute("""
        SELECT anunciante_id, similitud 
        FROM buscar_anunciante_fuzzy(%s, 80)
        LIMIT 1
    """, (nombre,))
    
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        return result[0], result[1]  # anunciante_id, similitud
    
    return None, 0

def agregar_alias_si_no_existe(conn, anunciante_id, nombre, fuente, confianza):
    """Agrega alias a la tabla si no existe"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dim_anunciante_aliases (anunciante_id, nombre_alias, fuente, confianza)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (nombre_alias) DO NOTHING
        """, (anunciante_id, nombre, fuente, confianza))
        conn.commit()
        cursor.close()
    except Exception as e:
        logger.warning(f"No se pudo agregar alias: {e}")

def cargar_inversion_medios(conn, file_path):
    """Carga fact_inversion_medios usando sistema de aliases"""
    print("\n" + "="*80)
    print("CARGANDO: Inversión en Medios 2024")
    print("="*80)
    
    # Leer Excel
    df = pd.read_excel(file_path)
    print(f"Total registros: {len(df):,}")
    
    # Preparar datos
    registros = []
    match_stats = {'matched': 0, 'fuzzy': 0, 'not_matched': 0}
    not_matched_names = set()
    nuevos_aliases = 0
    
    # Cache de búsquedas para no repetir
    nombre_cache = {}
    
    for idx, row in df.iterrows():
        nombre_anunciante = str(row['anunciante']).strip()
        
        # Usar cache
        if nombre_anunciante in nombre_cache:
            anunciante_id, confianza = nombre_cache[nombre_anunciante]
        else:
            # Buscar con sistema de aliases
            anunciante_id, confianza = buscar_anunciante_por_nombre(conn, nombre_anunciante)
            nombre_cache[nombre_anunciante] = (anunciante_id, confianza)
        
        if anunciante_id:
            if confianza == 100:
                match_stats['matched'] += 1
            else:
                match_stats['fuzzy'] += 1
            
            # Agregar alias si no existe (para futuros matches)
            agregar_alias_si_no_existe(conn, anunciante_id, nombre_anunciante, 'adlens_inversion', confianza)
            if confianza < 100:
                nuevos_aliases += 1
        else:
            match_stats['not_matched'] += 1
            not_matched_names.add(nombre_anunciante)
        
        # Manejar MES (puede venir como int, float o Timestamp)
        mes = None
        if pd.notna(row.get('MES')):
            try:
                if isinstance(row['MES'], pd.Timestamp):
                    mes = row['MES'].month
                else:
                    mes = int(float(row['MES']))
            except:
                mes = None
        
        # Manejar AÑO (puede venir como int, float o Timestamp)
        anio = None
        if pd.notna(row.get('AÑO')):
            try:
                if isinstance(row['AÑO'], pd.Timestamp):
                    anio = row['AÑO'].year
                else:
                    anio = int(float(row['AÑO']))
            except:
                anio = None
        
        # Función helper para convertir números con formato europeo
        def parse_float(value):
            if pd.isna(value):
                return 0.0
            if isinstance(value, (int, float)):
                return float(value)
            # Si es string, reemplazar coma por punto
            try:
                return float(str(value).replace(',', '.'))
            except:
                return 0.0
        
        registros.append((
            anunciante_id,
            row.get('Setor'),
            row.get('Categoria'),
            nombre_anunciante,
            row.get('Agência'),
            row.get('Medio'),
            row.get('Veículo'),
            row.get('Grupo Empresarial'),
            mes,
            anio,
            parse_float(row.get('(GS)')),
            parse_float(row.get('(US$)')),
            parse_float(row.get('Desc %')),
            parse_float(row.get('RANGO DE INVERSIÓN'))
        ))
        
        if (idx + 1) % 10000 == 0:
            print(f"  Procesados: {idx + 1:,}")
    
    # Insertar en BD
    print("\nInsertando en base de datos...")
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO fact_inversion_medios (
            anunciante_id, setor, categoria, nombre_anunciante, 
            agencia, medio, vehiculo, grupo_empresarial,
            mes, anio, monto_gs, monto_usd, descuento_pct, rango_inversion
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    execute_batch(cursor, insert_query, registros, page_size=1000)
    conn.commit()
    cursor.close()
    
    print(f"\n✅ {len(registros):,} registros insertados")
    print(f"✅ {nuevos_aliases} nuevos aliases agregados")
    print(f"\n📊 Estadísticas de matching:")
    print(f"   ✅ Match exacto: {match_stats['matched']:,} ({match_stats['matched']/len(df)*100:.1f}%)")
    print(f"   🔍 Match fuzzy: {match_stats['fuzzy']:,} ({match_stats['fuzzy']/len(df)*100:.1f}%)")
    print(f"   ❌ Sin match: {match_stats['not_matched']:,} ({match_stats['not_matched']/len(df)*100:.1f}%)")
    
    if not_matched_names:
        print(f"\n⚠️  Top 20 nombres sin match:")
        for i, name in enumerate(list(not_matched_names)[:20], 1):
            print(f"   {i}. {name}")

def cargar_posicionamiento_dnit(conn, file_path):
    """Carga dim_posicionamiento_dnit usando sistema de aliases"""
    print("\n" + "="*80)
    print("CARGANDO: Posicionamiento DNIT")
    print("="*80)
    
    # Leer Excel
    df = pd.read_excel(file_path)
    print(f"Total registros: {len(df):,}")
    
    # Preparar datos
    registros = []
    match_stats = {'matched': 0, 'fuzzy': 0, 'not_matched': 0}
    not_matched_names = set()
    nuevos_aliases = 0
    
    # Cache de búsquedas
    nombre_cache = {}
    
    for idx, row in df.iterrows():
        ruc = int(row['RUC']) if pd.notna(row.get('RUC')) else None
        razon_social = str(row['Razon_Social']).strip()
        
        # Usar cache
        if razon_social in nombre_cache:
            anunciante_id, confianza = nombre_cache[razon_social]
        else:
            # Buscar con sistema de aliases
            anunciante_id, confianza = buscar_anunciante_por_nombre(conn, razon_social)
            nombre_cache[razon_social] = (anunciante_id, confianza)
        
        if anunciante_id:
            if confianza == 100:
                match_stats['matched'] += 1
            else:
                match_stats['fuzzy'] += 1
            
            # Agregar alias si no existe
            agregar_alias_si_no_existe(conn, anunciante_id, razon_social, 'dnit', confianza)
            if confianza < 100:
                nuevos_aliases += 1
        else:
            match_stats['not_matched'] += 1
            not_matched_names.add(razon_social)
        
        # Función helper para convertir números
        def parse_float(value):
            if pd.isna(value):
                return 0.0
            if isinstance(value, (int, float)):
                return float(value)
            try:
                return float(str(value).replace(',', '.'))
            except:
                return 0.0
        
        registros.append((
            anunciante_id,
            int(row['Ranking']) if pd.notna(row.get('Ranking')) else None,
            ruc,
            razon_social,
            parse_float(row.get('Aporte en Guaraníes')),
            parse_float(row.get('Ingreso Estimado (Gs.)'))
        ))
    
    # Insertar en BD
    print("\nInsertando en base de datos...")
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO dim_posicionamiento_dnit (
            anunciante_id, ranking, ruc, razon_social, 
            aporte_gs, ingreso_estimado_gs
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (ruc) DO UPDATE SET
            anunciante_id = EXCLUDED.anunciante_id,
            ranking = EXCLUDED.ranking,
            razon_social = EXCLUDED.razon_social,
            aporte_gs = EXCLUDED.aporte_gs,
            ingreso_estimado_gs = EXCLUDED.ingreso_estimado_gs
    """
    
    execute_batch(cursor, insert_query, registros, page_size=1000)
    conn.commit()
    cursor.close()
    
    print(f"\n✅ {len(registros):,} registros insertados")
    print(f"✅ {nuevos_aliases} nuevos aliases agregados")
    print(f"\n📊 Estadísticas de matching:")
    print(f"   ✅ Match exacto: {match_stats['matched']:,}")
    print(f"   🔍 Match fuzzy: {match_stats['fuzzy']:,}")
    print(f"   ❌ Sin match: {match_stats['not_matched']:,}")
    
    if not_matched_names:
        print(f"\n⚠️  Top 20 nombres sin match:")
        for i, name in enumerate(list(not_matched_names)[:20], 1):
            print(f"   {i}. {name}")

def main():
    """Ejecutar carga completa"""
    print("\n🚀 INICIANDO CARGA DE DATOS")
    print("="*80)
    
    try:
        # Conectar a BD
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conectado a PostgreSQL")
        
        # Cargar Inversión en Medios
        cargar_inversion_medios(
            conn, 
            "Inversion_en_medios_2024_-_Adlens.xlsx"
        )
        
        # Cargar Posicionamiento DNIT
        cargar_posicionamiento_dnit(
            conn,
            "POSICIONAMIENTO_DE_CLIENTES.xlsx"
        )
        
        conn.close()
        print("\n" + "="*80)
        print("✅ CARGA COMPLETADA EXITOSAMENTE")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise

if __name__ == "__main__":
    main()