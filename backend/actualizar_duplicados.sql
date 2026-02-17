-- ACTUALIZAR CLIENTES DUPLICADOS
-- Mapear clientes faltantes a anunciantes existentes

-- AMANECER S.A -> AMANECER SA (ID: 58)
UPDATE fact_facturacion 
SET anunciante_id = 58 
WHERE cliente_original = 'AMANECER S.A';

