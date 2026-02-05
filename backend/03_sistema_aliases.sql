-- ============================================================================
-- SISTEMA DE ALIASES - Mapeo Centralizado de Nombres de Clientes
-- Solución para que "CERVEPAR", "cervepar", "CERVEPAR S.A." apunten al mismo cliente
-- ============================================================================

-- TABLA: dim_anunciante_aliases
-- ============================================================================
DROP TABLE IF EXISTS dim_anunciante_aliases CASCADE;

CREATE TABLE dim_anunciante_aliases (
    alias_id SERIAL PRIMARY KEY,
    anunciante_id INTEGER NOT NULL REFERENCES dim_anunciante(anunciante_id) ON DELETE CASCADE,
    nombre_alias VARCHAR(300) NOT NULL,
    fuente VARCHAR(50) NOT NULL, -- 'base', 'manual', 'adlens', 'dnit', 'facturacion', 'user_query'
    confianza INTEGER DEFAULT 100, -- 100 = exacto, 80-99 = fuzzy match, <80 = requiere validación
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100),
    CONSTRAINT unique_alias UNIQUE(nombre_alias)
);

CREATE INDEX idx_aliases_anunciante ON dim_anunciante_aliases(anunciante_id);
CREATE INDEX idx_aliases_nombre_upper ON dim_anunciante_aliases(UPPER(nombre_alias));
CREATE INDEX idx_aliases_fuente ON dim_anunciante_aliases(fuente);
CREATE INDEX idx_aliases_confianza ON dim_anunciante_aliases(confianza);

COMMENT ON TABLE dim_anunciante_aliases IS 
'Mapeo de todos los nombres posibles de un cliente a un anunciante_id único. 
Permite búsquedas flexibles: CERVEPAR, cervepar, CERVEPAR S.A. → mismo cliente';


-- FUNCIÓN: buscar_anunciante (búsqueda exacta en aliases)
-- ============================================================================
CREATE OR REPLACE FUNCTION buscar_anunciante(p_nombre TEXT)
RETURNS INTEGER AS $$
DECLARE
    v_anunciante_id INTEGER;
BEGIN
    -- Búsqueda case-insensitive en aliases
    SELECT anunciante_id INTO v_anunciante_id
    FROM dim_anunciante_aliases
    WHERE UPPER(TRIM(nombre_alias)) = UPPER(TRIM(p_nombre))
    ORDER BY confianza DESC, created_at DESC
    LIMIT 1;
    
    RETURN v_anunciante_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION buscar_anunciante IS 
'Busca anunciante_id por nombre. Case-insensitive. Prioriza por confianza.';


-- FUNCIÓN: buscar_anunciante_fuzzy (búsqueda con similitud)
-- ============================================================================
CREATE OR REPLACE FUNCTION buscar_anunciante_fuzzy(
    p_nombre TEXT,
    p_threshold INTEGER DEFAULT 80
)
RETURNS TABLE(
    anunciante_id INTEGER,
    nombre_alias VARCHAR,
    similitud INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.anunciante_id,
        a.nombre_alias,
        -- Simulación de similitud (en producción usar extensión pg_trgm)
        CASE 
            WHEN UPPER(a.nombre_alias) = UPPER(p_nombre) THEN 100
            WHEN UPPER(a.nombre_alias) LIKE '%' || UPPER(p_nombre) || '%' THEN 90
            WHEN UPPER(p_nombre) LIKE '%' || UPPER(a.nombre_alias) || '%' THEN 85
            ELSE 70
        END as similitud
    FROM dim_anunciante_aliases a
    WHERE 
        UPPER(a.nombre_alias) LIKE '%' || UPPER(p_nombre) || '%'
        OR UPPER(p_nombre) LIKE '%' || UPPER(a.nombre_alias) || '%'
    ORDER BY similitud DESC, a.confianza DESC
    LIMIT 5;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION buscar_anunciante_fuzzy IS 
'Búsqueda fuzzy que retorna top 5 matches con score de similitud.';


-- POBLACIÓN INICIAL: Aliases desde dim_anunciante
-- ============================================================================
INSERT INTO dim_anunciante_aliases (anunciante_id, nombre_alias, fuente, confianza)
SELECT 
    anunciante_id, 
    nombre_canonico, 
    'base',
    100
FROM dim_anunciante
ON CONFLICT (nombre_alias) DO NOTHING;


-- POBLACIÓN AUTOMÁTICA: Variaciones comunes
-- ============================================================================

-- Variación 1: Sin sufijos corporativos (S.A., S.A.E., LTDA, etc.)
INSERT INTO dim_anunciante_aliases (anunciante_id, nombre_alias, fuente, confianza)
SELECT 
    anunciante_id,
    TRIM(REGEXP_REPLACE(
        nombre_canonico, 
        '\s+(S\.?A\.?E?\.?|LTDA\.?|S\.?R\.?L\.?|SOCIEDAD ANONIMA)$', 
        '', 
        'i'
    )),
    'variacion_sin_sufijo',
    95
FROM dim_anunciante
WHERE nombre_canonico ~* '\s+(S\.?A\.?E?\.?|LTDA\.?|S\.?R\.?L\.?|SOCIEDAD ANONIMA)$'
ON CONFLICT (nombre_alias) DO NOTHING;


-- Variación 2: Minúsculas (para búsquedas de usuarios)
INSERT INTO dim_anunciante_aliases (anunciante_id, nombre_alias, fuente, confianza)
SELECT 
    anunciante_id,
    LOWER(nombre_canonico),
    'variacion_lowercase',
    95
FROM dim_anunciante
ON CONFLICT (nombre_alias) DO NOTHING;


-- Variación 3: Sin puntos ni espacios extra
INSERT INTO dim_anunciante_aliases (anunciante_id, nombre_alias, fuente, confianza)
SELECT 
    anunciante_id,
    REGEXP_REPLACE(
        REGEXP_REPLACE(nombre_canonico, '\.', '', 'g'),
        '\s+', ' ', 'g'
    ),
    'variacion_sin_puntos',
    90
FROM dim_anunciante
ON CONFLICT (nombre_alias) DO NOTHING;


-- ============================================================================
-- VISTAS ÚTILES
-- ============================================================================

-- Vista: Clientes con todos sus aliases
CREATE OR REPLACE VIEW v_anunciantes_con_aliases AS
SELECT 
    d.anunciante_id,
    d.nombre_canonico,
    COUNT(a.alias_id) as total_aliases,
    STRING_AGG(a.nombre_alias, ' | ' ORDER BY a.confianza DESC) as todos_los_aliases
FROM dim_anunciante d
LEFT JOIN dim_anunciante_aliases a ON d.anunciante_id = a.anunciante_id
GROUP BY d.anunciante_id, d.nombre_canonico;

COMMENT ON VIEW v_anunciantes_con_aliases IS 
'Vista consolidada: cada cliente con todos sus nombres/aliases conocidos.';


-- Vista: Aliases sin asignar (requieren revisión manual)
CREATE OR REPLACE VIEW v_aliases_pendientes AS
SELECT 
    alias_id,
    nombre_alias,
    fuente,
    confianza,
    created_at
FROM dim_anunciante_aliases
WHERE confianza < 80
ORDER BY created_at DESC;

COMMENT ON VIEW v_aliases_pendientes IS 
'Aliases con baja confianza que requieren validación manual del administrador.';


-- ============================================================================
-- QUERIES DE VALIDACIÓN
-- ============================================================================

-- Ver aliases de un cliente específico
-- SELECT * FROM dim_anunciante_aliases WHERE anunciante_id = 1;

-- Buscar cliente por cualquier nombre
-- SELECT buscar_anunciante('cervepar');
-- SELECT buscar_anunciante('CERVEPAR S.A.');

-- Búsqueda fuzzy
-- SELECT * FROM buscar_anunciante_fuzzy('cerve', 70);

-- Ver clientes con más aliases
-- SELECT * FROM v_anunciantes_con_aliases ORDER BY total_aliases DESC LIMIT 10;

-- Ver aliases pendientes de validación
-- SELECT * FROM v_aliases_pendientes;


-- ============================================================================
-- ESTADÍSTICAS
-- ============================================================================
SELECT 
    'Total Anunciantes' as metrica,
    COUNT(*) as valor
FROM dim_anunciante
UNION ALL
SELECT 
    'Total Aliases',
    COUNT(*)
FROM dim_anunciante_aliases
UNION ALL
SELECT 
    'Aliases por Cliente (promedio)',
    ROUND(AVG(alias_count), 2)
FROM (
    SELECT COUNT(*) as alias_count
    FROM dim_anunciante_aliases
    GROUP BY anunciante_id
) subq;


-- ============================================================================
-- EJEMPLO DE USO EN QUERIES
-- ============================================================================

/*
ANTES (sin aliases):
SELECT * FROM fact_facturacion f
JOIN dim_anunciante d ON f.anunciante_id = d.anunciante_id
WHERE d.nombre_canonico = 'CERVEPAR S.A.';  -- Solo funciona con nombre exacto

DESPUÉS (con aliases):
SELECT * FROM fact_facturacion f
WHERE f.anunciante_id = buscar_anunciante('cervepar');  -- Funciona con cualquier variación
*/
