-- CREAR NUEVOS ANUNCIANTES
-- Insertar anunciantes completamente nuevos

-- TELEFONICA CELULAR DEL PARAGUAY S.A.E. - 9,213,656,412 Gs (186 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1000, 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.');
UPDATE fact_facturacion 
SET anunciante_id = 1000 
WHERE cliente_original = 'TELEFONICA CELULAR DEL PARAGUAY S.A.E.';

-- AISANI S.A - 4,036,856,062 Gs (330 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1001, 'AISANI S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1001 
WHERE cliente_original = 'AISANI S.A';

-- EDURED GROUP S.A. - 3,723,575,507 Gs (158 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1002, 'EDURED GROUP S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1002 
WHERE cliente_original = 'EDURED GROUP S.A.';

-- PEPSICO DEL PARAGUAY S.R.L. - 3,572,912,716 Gs (135 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1003, 'PEPSICO DEL PARAGUAY S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1003 
WHERE cliente_original = 'PEPSICO DEL PARAGUAY S.R.L.';

-- COATI S.A. - 2,222,117,893 Gs (203 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1004, 'COATI S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1004 
WHERE cliente_original = 'COATI S.A.';

-- NGO SAECA - 1,928,686,190 Gs (188 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1005, 'NGO SAECA');
UPDATE fact_facturacion 
SET anunciante_id = 1005 
WHERE cliente_original = 'NGO SAECA';

-- TRAMONTINA COMERCIALIZACIÓN Y REPR. URUGUAY SA - 1,537,356,755 Gs (54 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1006, 'TRAMONTINA COMERCIALIZACIÓN Y REPR. URUGUAY SA');
UPDATE fact_facturacion 
SET anunciante_id = 1006 
WHERE cliente_original = 'TRAMONTINA COMERCIALIZACIÓN Y REPR. URUGUAY SA';

-- DIAGEO PARAGUAY SRL - 1,265,532,317 Gs (130 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1007, 'DIAGEO PARAGUAY SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1007 
WHERE cliente_original = 'DIAGEO PARAGUAY SRL';

-- LG ELECTRONICS PERU SA SUCURSAL PARAGUAY - 1,255,173,369 Gs (559 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1008, 'LG ELECTRONICS PERU SA SUCURSAL PARAGUAY');
UPDATE fact_facturacion 
SET anunciante_id = 1008 
WHERE cliente_original = 'LG ELECTRONICS PERU SA SUCURSAL PARAGUAY';

-- DIGITAL HIVE GROUP E.A.S. - 1,140,224,462 Gs (56 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1009, 'DIGITAL HIVE GROUP E.A.S.');
UPDATE fact_facturacion 
SET anunciante_id = 1009 
WHERE cliente_original = 'DIGITAL HIVE GROUP E.A.S.';

-- INMOBILIARIA RAICES S.A - 817,649,504 Gs (132 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1010, 'INMOBILIARIA RAICES S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1010 
WHERE cliente_original = 'INMOBILIARIA RAICES S.A';

-- NTU INTERNATIONAL A/S - 727,535,474 Gs (17 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1011, 'NTU INTERNATIONAL A/S');
UPDATE fact_facturacion 
SET anunciante_id = 1011 
WHERE cliente_original = 'NTU INTERNATIONAL A/S';

-- INDEX SACI - 680,061,342 Gs (39 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1012, 'INDEX SACI');
UPDATE fact_facturacion 
SET anunciante_id = 1012 
WHERE cliente_original = 'INDEX SACI';

-- BOLT OPERATIONS OÜ - 664,280,106 Gs (7 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1013, 'BOLT OPERATIONS OÜ');
UPDATE fact_facturacion 
SET anunciante_id = 1013 
WHERE cliente_original = 'BOLT OPERATIONS OÜ';

-- CREDITO VERDE SA - 661,715,164 Gs (25 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1014, 'CREDITO VERDE SA');
UPDATE fact_facturacion 
SET anunciante_id = 1014 
WHERE cliente_original = 'CREDITO VERDE SA';

-- LAISTAR S.A. - 660,480,755 Gs (34 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1015, 'LAISTAR S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1015 
WHERE cliente_original = 'LAISTAR S.A.';

-- GRUPO CELL MOTION S.A. - 573,171,352 Gs (13 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1016, 'GRUPO CELL MOTION S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1016 
WHERE cliente_original = 'GRUPO CELL MOTION S.A.';

-- YP S.A - 531,213,049 Gs (81 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1017, 'YP S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1017 
WHERE cliente_original = 'YP S.A';

-- LABORATORIO DE PRODUCTOS ETICOS CEISA - 530,631,284 Gs (80 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1018, 'LABORATORIO DE PRODUCTOS ETICOS CEISA');
UPDATE fact_facturacion 
SET anunciante_id = 1018 
WHERE cliente_original = 'LABORATORIO DE PRODUCTOS ETICOS CEISA';

-- FAMILIAR SEGUROS S.A. - 515,849,871 Gs (89 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1019, 'FAMILIAR SEGUROS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1019 
WHERE cliente_original = 'FAMILIAR SEGUROS S.A.';

-- INDUSTRIA PAPELERA URUGUAYA SA - 515,099,176 Gs (16 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1020, 'INDUSTRIA PAPELERA URUGUAYA SA');
UPDATE fact_facturacion 
SET anunciante_id = 1020 
WHERE cliente_original = 'INDUSTRIA PAPELERA URUGUAYA SA';

-- WINES AND SPIRITS S.A. - 510,877,762 Gs (15 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1021, 'WINES AND SPIRITS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1021 
WHERE cliente_original = 'WINES AND SPIRITS S.A.';

-- DIESA S.A. - 501,331,816 Gs (93 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1022, 'DIESA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1022 
WHERE cliente_original = 'DIESA S.A.';

-- FOCUS MEDIA S.A - 491,431,689 Gs (65 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1023, 'FOCUS MEDIA S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1023 
WHERE cliente_original = 'FOCUS MEDIA S.A';

-- BIG BANG S.A. - 452,175,235 Gs (10 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1024, 'BIG BANG S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1024 
WHERE cliente_original = 'BIG BANG S.A.';

-- BRICK S.A. - 401,647,669 Gs (28 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1025, 'BRICK S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1025 
WHERE cliente_original = 'BRICK S.A.';

-- PROJECT S.A. (LG) - 396,199,961 Gs (34 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1026, 'PROJECT S.A. (LG)');
UPDATE fact_facturacion 
SET anunciante_id = 1026 
WHERE cliente_original = 'PROJECT S.A. (LG)';

-- GLORIA S.A.C.E.I - 374,263,599 Gs (112 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1027, 'GLORIA S.A.C.E.I');
UPDATE fact_facturacion 
SET anunciante_id = 1027 
WHERE cliente_original = 'GLORIA S.A.C.E.I';

-- HONOR INFORMATION TECHNOLOGY CO., LIMITED - 368,244,504 Gs (31 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1028, 'HONOR INFORMATION TECHNOLOGY CO., LIMITED');
UPDATE fact_facturacion 
SET anunciante_id = 1028 
WHERE cliente_original = 'HONOR INFORMATION TECHNOLOGY CO., LIMITED';

-- RAMPER PARAGUAY S.A - 354,457,730 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1029, 'RAMPER PARAGUAY S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1029 
WHERE cliente_original = 'RAMPER PARAGUAY S.A';

-- PUBLICITARIA NASTA S.A. - 326,591,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1030, 'PUBLICITARIA NASTA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1030 
WHERE cliente_original = 'PUBLICITARIA NASTA S.A.';

-- RUOTI & CÍA S.A. - 274,560,783 Gs (37 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1031, 'RUOTI & CÍA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1031 
WHERE cliente_original = 'RUOTI & CÍA S.A.';

-- PRIME INVESTMENTS S.A. - 264,045,698 Gs (52 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1032, 'PRIME INVESTMENTS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1032 
WHERE cliente_original = 'PRIME INVESTMENTS S.A.';

-- AJ S.A. CALIDAD ANTE TODO - 259,637,590 Gs (13 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1033, 'AJ S.A. CALIDAD ANTE TODO');
UPDATE fact_facturacion 
SET anunciante_id = 1033 
WHERE cliente_original = 'AJ S.A. CALIDAD ANTE TODO';

-- BASA CASA DE BOLSA SA - 253,834,192 Gs (32 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1034, 'BASA CASA DE BOLSA SA');
UPDATE fact_facturacion 
SET anunciante_id = 1034 
WHERE cliente_original = 'BASA CASA DE BOLSA SA';

-- ENE S.A - 247,926,665 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1035, 'ENE S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1035 
WHERE cliente_original = 'ENE S.A';

-- KENVUE PARAGUAY SA - 234,900,338 Gs (16 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1036, 'KENVUE PARAGUAY SA');
UPDATE fact_facturacion 
SET anunciante_id = 1036 
WHERE cliente_original = 'KENVUE PARAGUAY SA';

-- CONFORT PARA EL HOGAR S.A. - 221,809,044 Gs (20 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1037, 'CONFORT PARA EL HOGAR S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1037 
WHERE cliente_original = 'CONFORT PARA EL HOGAR S.A.';

-- FUNDACION PARQUE TECNOLOGICO ITAIPU - PY - 187,550,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1038, 'FUNDACION PARQUE TECNOLOGICO ITAIPU - PY');
UPDATE fact_facturacion 
SET anunciante_id = 1038 
WHERE cliente_original = 'FUNDACION PARQUE TECNOLOGICO ITAIPU - PY';

-- MASS MEDIA S.A. - 177,412,453 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1039, 'MASS MEDIA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1039 
WHERE cliente_original = 'MASS MEDIA S.A.';

-- BIEDERMANN PUBLICIDAD S.A - 172,990,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1040, 'BIEDERMANN PUBLICIDAD S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1040 
WHERE cliente_original = 'BIEDERMANN PUBLICIDAD S.A';

-- CAMARA PYA.DE PROC.DE OLEAG.Y CEREALESCAPPRO - 163,271,699 Gs (32 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1041, 'CAMARA PYA.DE PROC.DE OLEAG.Y CEREALESCAPPRO');
UPDATE fact_facturacion 
SET anunciante_id = 1041 
WHERE cliente_original = 'CAMARA PYA.DE PROC.DE OLEAG.Y CEREALESCAPPRO';

-- TORDESILLAS S.A. - 159,053,100 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1042, 'TORDESILLAS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1042 
WHERE cliente_original = 'TORDESILLAS S.A.';

-- JWF S.A. - 156,094,595 Gs (27 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1043, 'JWF S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1043 
WHERE cliente_original = 'JWF S.A.';

-- SERVICIOS RÁPIDOS DEL PARAGUAY SA - 150,915,088 Gs (20 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1044, 'SERVICIOS RÁPIDOS DEL PARAGUAY SA');
UPDATE fact_facturacion 
SET anunciante_id = 1044 
WHERE cliente_original = 'SERVICIOS RÁPIDOS DEL PARAGUAY SA';

-- FAMILIAR AFPI S.A - 150,562,152 Gs (67 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1045, 'FAMILIAR AFPI S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1045 
WHERE cliente_original = 'FAMILIAR AFPI S.A';

-- CORP PYA DISTRI DE DERIV DE PETROLEO SA - 138,076,727 Gs (11 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1046, 'CORP PYA DISTRI DE DERIV DE PETROLEO SA');
UPDATE fact_facturacion 
SET anunciante_id = 1046 
WHERE cliente_original = 'CORP PYA DISTRI DE DERIV DE PETROLEO SA';

-- ONIRIA S.A - 133,015,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1047, 'ONIRIA S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1047 
WHERE cliente_original = 'ONIRIA S.A';

-- NATANIA PARAGUAY S.A - 130,626,592 Gs (30 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1048, 'NATANIA PARAGUAY S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1048 
WHERE cliente_original = 'NATANIA PARAGUAY S.A';

-- IMPLENIA SA - 126,742,400 Gs (21 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1049, 'IMPLENIA SA');
UPDATE fact_facturacion 
SET anunciante_id = 1049 
WHERE cliente_original = 'IMPLENIA SA';

-- FENEDUR S.A - 120,441,796 Gs (20 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1050, 'FENEDUR S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1050 
WHERE cliente_original = 'FENEDUR S.A';

-- TEXO S.A. - 120,195,778 Gs (64 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1051, 'TEXO S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1051 
WHERE cliente_original = 'TEXO S.A.';

-- DIRECCIÓN ÓPTIMA DE MEDIOS SRL - 113,729,934 Gs (50 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1052, 'DIRECCIÓN ÓPTIMA DE MEDIOS SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1052 
WHERE cliente_original = 'DIRECCIÓN ÓPTIMA DE MEDIOS SRL';

-- FILMAGIC S.A. - 109,816,670 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1053, 'FILMAGIC S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1053 
WHERE cliente_original = 'FILMAGIC S.A.';

-- CEREALES SA - 109,045,925 Gs (18 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1054, 'CEREALES SA');
UPDATE fact_facturacion 
SET anunciante_id = 1054 
WHERE cliente_original = 'CEREALES SA';

-- BELLCOS SA - 107,796,286 Gs (45 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1055, 'BELLCOS SA');
UPDATE fact_facturacion 
SET anunciante_id = 1055 
WHERE cliente_original = 'BELLCOS SA';

-- TIGRE PARAGUAY S.A - 104,487,991 Gs (18 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1056, 'TIGRE PARAGUAY S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1056 
WHERE cliente_original = 'TIGRE PARAGUAY S.A';

-- RIMEC S.A.C.I. - 102,461,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1057, 'RIMEC S.A.C.I.');
UPDATE fact_facturacion 
SET anunciante_id = 1057 
WHERE cliente_original = 'RIMEC S.A.C.I.';

-- WORLD WILDLIFE FUND.INC.(WWF) - 100,851,775 Gs (11 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1058, 'WORLD WILDLIFE FUND.INC.(WWF)');
UPDATE fact_facturacion 
SET anunciante_id = 1058 
WHERE cliente_original = 'WORLD WILDLIFE FUND.INC.(WWF)';

-- INTERBORDERS SRL - 100,849,440 Gs (8 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1059, 'INTERBORDERS SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1059 
WHERE cliente_original = 'INTERBORDERS SRL';

-- RAIZEN PARAGUAY SA - 100,687,520 Gs (16 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1060, 'RAIZEN PARAGUAY SA');
UPDATE fact_facturacion 
SET anunciante_id = 1060 
WHERE cliente_original = 'RAIZEN PARAGUAY SA';

-- AMNISTIA INTERNACIONAL PARAGUAY. - 89,429,773 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1061, 'AMNISTIA INTERNACIONAL PARAGUAY.');
UPDATE fact_facturacion 
SET anunciante_id = 1061 
WHERE cliente_original = 'AMNISTIA INTERNACIONAL PARAGUAY.';

-- RECORD ELECTRIC S.A.E.C.A. - 88,430,000 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1062, 'RECORD ELECTRIC S.A.E.C.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1062 
WHERE cliente_original = 'RECORD ELECTRIC S.A.E.C.A.';

-- IGNIS M&C S.A. - 87,353,085 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1063, 'IGNIS M&C S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1063 
WHERE cliente_original = 'IGNIS M&C S.A.';

-- ATOMIK PRO - 86,228,010 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1064, 'ATOMIK PRO');
UPDATE fact_facturacion 
SET anunciante_id = 1064 
WHERE cliente_original = 'ATOMIK PRO';

-- TELEVISION CERRO CORA S.A. - 85,986,882 Gs (8 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1065, 'TELEVISION CERRO CORA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1065 
WHERE cliente_original = 'TELEVISION CERRO CORA S.A.';

-- DISTRI REP S.R.L. - 84,489,058 Gs (11 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1066, 'DISTRI REP S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1066 
WHERE cliente_original = 'DISTRI REP S.R.L.';

-- VIA PUBLICA S.A.C.I. - 80,246,332 Gs (46 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1067, 'VIA PUBLICA S.A.C.I.');
UPDATE fact_facturacion 
SET anunciante_id = 1067 
WHERE cliente_original = 'VIA PUBLICA S.A.C.I.';

-- OFICINA DEL COORD. RESIDENTE DE LA ORG. DE LAS NNU - 73,870,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1068, 'OFICINA DEL COORD. RESIDENTE DE LA ORG. DE LAS NNU');
UPDATE fact_facturacion 
SET anunciante_id = 1068 
WHERE cliente_original = 'OFICINA DEL COORD. RESIDENTE DE LA ORG. DE LAS NNU';

-- STRATEGY LATAM SA - 72,525,095 Gs (15 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1069, 'STRATEGY LATAM SA');
UPDATE fact_facturacion 
SET anunciante_id = 1069 
WHERE cliente_original = 'STRATEGY LATAM SA';

-- MEDIABRAND S.A. - 70,853,911 Gs (10 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1070, 'MEDIABRAND S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1070 
WHERE cliente_original = 'MEDIABRAND S.A.';

-- PHD CHILE SA - 67,431,357 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1071, 'PHD CHILE SA');
UPDATE fact_facturacion 
SET anunciante_id = 1071 
WHERE cliente_original = 'PHD CHILE SA';

-- GRUPO J 10 SA - 66,520,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1072, 'GRUPO J 10 SA');
UPDATE fact_facturacion 
SET anunciante_id = 1072 
WHERE cliente_original = 'GRUPO J 10 SA';

-- LGN ADVERTISING GROUP SA - 66,509,559 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1073, 'LGN ADVERTISING GROUP SA');
UPDATE fact_facturacion 
SET anunciante_id = 1073 
WHERE cliente_original = 'LGN ADVERTISING GROUP SA';

-- UNION  S.R.L - 66,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1074, 'UNION  S.R.L');
UPDATE fact_facturacion 
SET anunciante_id = 1074 
WHERE cliente_original = 'UNION  S.R.L';

-- PROTEK S.R.L - 65,926,217 Gs (25 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1075, 'PROTEK S.R.L');
UPDATE fact_facturacion 
SET anunciante_id = 1075 
WHERE cliente_original = 'PROTEK S.R.L';

-- PERSONAL ENVIOS S.A. - 65,000,000 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1076, 'PERSONAL ENVIOS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1076 
WHERE cliente_original = 'PERSONAL ENVIOS S.A.';

-- OGILVY & MATHER COLOMBIA S.A.S. - 64,085,794 Gs (19 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1077, 'OGILVY & MATHER COLOMBIA S.A.S.');
UPDATE fact_facturacion 
SET anunciante_id = 1077 
WHERE cliente_original = 'OGILVY & MATHER COLOMBIA S.A.S.';

-- EVENTUALLY APS - 63,490,915 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1078, 'EVENTUALLY APS');
UPDATE fact_facturacion 
SET anunciante_id = 1078 
WHERE cliente_original = 'EVENTUALLY APS';

-- CARMOTOR PARAGUAY S.A - 59,332,796 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1079, 'CARMOTOR PARAGUAY S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1079 
WHERE cliente_original = 'CARMOTOR PARAGUAY S.A';

-- LA PERSEVERANCIA, P.ZUCOLILLO SA - 55,514,244 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1080, 'LA PERSEVERANCIA, P.ZUCOLILLO SA');
UPDATE fact_facturacion 
SET anunciante_id = 1080 
WHERE cliente_original = 'LA PERSEVERANCIA, P.ZUCOLILLO SA';

-- MOBILE CASH PARAGUAY S.A - 55,455,175 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1081, 'MOBILE CASH PARAGUAY S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1081 
WHERE cliente_original = 'MOBILE CASH PARAGUAY S.A';

-- MERCOSUR SPORTS WORLD CORPORATION - 53,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1082, 'MERCOSUR SPORTS WORLD CORPORATION');
UPDATE fact_facturacion 
SET anunciante_id = 1082 
WHERE cliente_original = 'MERCOSUR SPORTS WORLD CORPORATION';

-- INCADE S.A.E. - 51,099,801 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1083, 'INCADE S.A.E.');
UPDATE fact_facturacion 
SET anunciante_id = 1083 
WHERE cliente_original = 'INCADE S.A.E.';

-- CESAR CARLOS DIAZ BELTRAN EIRL - 49,571,114 Gs (24 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1084, 'CESAR CARLOS DIAZ BELTRAN EIRL');
UPDATE fact_facturacion 
SET anunciante_id = 1084 
WHERE cliente_original = 'CESAR CARLOS DIAZ BELTRAN EIRL';

-- COMFAR S.A.E.C.A. - 49,000,000 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1085, 'COMFAR S.A.E.C.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1085 
WHERE cliente_original = 'COMFAR S.A.E.C.A.';

-- ENTRETENIMIENTOS DEL SUR S.A. - 47,897,190 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1086, 'ENTRETENIMIENTOS DEL SUR S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1086 
WHERE cliente_original = 'ENTRETENIMIENTOS DEL SUR S.A.';

-- P & M GROUP S.R.L. - 47,875,455 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1087, 'P & M GROUP S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1087 
WHERE cliente_original = 'P & M GROUP S.R.L.';

-- CAFÉ SIRENA PARAGUAY S.A - 47,327,190 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1088, 'CAFÉ SIRENA PARAGUAY S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1088 
WHERE cliente_original = 'CAFÉ SIRENA PARAGUAY S.A';

-- EDITORIAL DE NEGOCIOS S.A. - 46,299,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1089, 'EDITORIAL DE NEGOCIOS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1089 
WHERE cliente_original = 'EDITORIAL DE NEGOCIOS S.A.';

-- PROTECCION MEDICA SA (PROMED SA) - 39,233,845 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1090, 'PROTECCION MEDICA SA (PROMED SA)');
UPDATE fact_facturacion 
SET anunciante_id = 1090 
WHERE cliente_original = 'PROTECCION MEDICA SA (PROMED SA)';

-- LA MEDIA DE LUPE S.A. - 38,857,378 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1091, 'LA MEDIA DE LUPE S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1091 
WHERE cliente_original = 'LA MEDIA DE LUPE S.A.';

-- BLUE TOWER VENTURES PARAGUAY S.A. - 38,670,447 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1092, 'BLUE TOWER VENTURES PARAGUAY S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1092 
WHERE cliente_original = 'BLUE TOWER VENTURES PARAGUAY S.A.';

-- TV ACCION S.A. - 36,177,072 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1093, 'TV ACCION S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1093 
WHERE cliente_original = 'TV ACCION S.A.';

-- SALUD CONCORDIA SA - 35,880,000 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1094, 'SALUD CONCORDIA SA');
UPDATE fact_facturacion 
SET anunciante_id = 1094 
WHERE cliente_original = 'SALUD CONCORDIA SA';

-- BRANDING BURGO S.A. - 35,329,455 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1095, 'BRANDING BURGO S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1095 
WHERE cliente_original = 'BRANDING BURGO S.A.';

-- AMAMBAY INGENIERIA S.A - 35,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1096, 'AMAMBAY INGENIERIA S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1096 
WHERE cliente_original = 'AMAMBAY INGENIERIA S.A';

-- PIROY S.A. - 34,181,818 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1097, 'PIROY S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1097 
WHERE cliente_original = 'PIROY S.A.';

-- A. MARTINEZ E HIJOS SAC - 33,280,942 Gs (9 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1098, 'A. MARTINEZ E HIJOS SAC');
UPDATE fact_facturacion 
SET anunciante_id = 1098 
WHERE cliente_original = 'A. MARTINEZ E HIJOS SAC';

-- MUSTER S.A. - 33,200,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1099, 'MUSTER S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1099 
WHERE cliente_original = 'MUSTER S.A.';

-- JETSMART SPA - 32,179,900 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1100, 'JETSMART SPA');
UPDATE fact_facturacion 
SET anunciante_id = 1100 
WHERE cliente_original = 'JETSMART SPA';

-- DOXA CONSTRUYE S.A - 31,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1101, 'DOXA CONSTRUYE S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1101 
WHERE cliente_original = 'DOXA CONSTRUYE S.A';

-- RGA SA TECNOLOGIA Y SERVICIO - 30,681,818 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1102, 'RGA SA TECNOLOGIA Y SERVICIO');
UPDATE fact_facturacion 
SET anunciante_id = 1102 
WHERE cliente_original = 'RGA SA TECNOLOGIA Y SERVICIO';

-- SPORT GROUP SA - 30,300,885 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1103, 'SPORT GROUP SA');
UPDATE fact_facturacion 
SET anunciante_id = 1103 
WHERE cliente_original = 'SPORT GROUP SA';

-- FORTALEZA INMUEBLES SAE - 30,000,000 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1104, 'FORTALEZA INMUEBLES SAE');
UPDATE fact_facturacion 
SET anunciante_id = 1104 
WHERE cliente_original = 'FORTALEZA INMUEBLES SAE';

-- ESCALA PTK S.A - 29,479,892 Gs (18 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1105, 'ESCALA PTK S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1105 
WHERE cliente_original = 'ESCALA PTK S.A';

-- CORPORACION DEL SUR S.A. - 28,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1106, 'CORPORACION DEL SUR S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1106 
WHERE cliente_original = 'CORPORACION DEL SUR S.A.';

-- MEDIA ADVANCED PLANNING S.A. - 28,435,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1107, 'MEDIA ADVANCED PLANNING S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1107 
WHERE cliente_original = 'MEDIA ADVANCED PLANNING S.A.';

-- FLORENTIN ROJAS, PAOLA ALEJANDRA - 28,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1108, 'FLORENTIN ROJAS, PAOLA ALEJANDRA');
UPDATE fact_facturacion 
SET anunciante_id = 1108 
WHERE cliente_original = 'FLORENTIN ROJAS, PAOLA ALEJANDRA';

-- VIA PÚBLICA S.A.C.I. - 26,970,000 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1109, 'VIA PÚBLICA S.A.C.I.');
UPDATE fact_facturacion 
SET anunciante_id = 1109 
WHERE cliente_original = 'VIA PÚBLICA S.A.C.I.';

-- CAPRONI S.A. - 26,819,000 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1110, 'CAPRONI S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1110 
WHERE cliente_original = 'CAPRONI S.A.';

-- CIA. EMBOTELLADORA TRES LEONES I.C.S.A. - 26,730,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1111, 'CIA. EMBOTELLADORA TRES LEONES I.C.S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1111 
WHERE cliente_original = 'CIA. EMBOTELLADORA TRES LEONES I.C.S.A.';

-- AC IMPORTACIONES S.A - 26,500,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1112, 'AC IMPORTACIONES S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1112 
WHERE cliente_original = 'AC IMPORTACIONES S.A';

-- UNIVERSIDAD SAN CARLOS - 26,198,485 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1113, 'UNIVERSIDAD SAN CARLOS');
UPDATE fact_facturacion 
SET anunciante_id = 1113 
WHERE cliente_original = 'UNIVERSIDAD SAN CARLOS';

-- BASA SEGUROS SA - 26,000,000 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1114, 'BASA SEGUROS SA');
UPDATE fact_facturacion 
SET anunciante_id = 1114 
WHERE cliente_original = 'BASA SEGUROS SA';

-- HIGHLANDS PARK & LAGOON SA - 24,150,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1115, 'HIGHLANDS PARK & LAGOON SA');
UPDATE fact_facturacion 
SET anunciante_id = 1115 
WHERE cliente_original = 'HIGHLANDS PARK & LAGOON SA';

-- HH GLOBAL PARAGUAY SA - 23,461,925 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1116, 'HH GLOBAL PARAGUAY SA');
UPDATE fact_facturacion 
SET anunciante_id = 1116 
WHERE cliente_original = 'HH GLOBAL PARAGUAY SA';

-- AMPM  S.A - 23,430,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1117, 'AMPM  S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1117 
WHERE cliente_original = 'AMPM  S.A';

-- APOLO 11 PUBLICITARIA SRL - 22,827,273 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1118, 'APOLO 11 PUBLICITARIA SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1118 
WHERE cliente_original = 'APOLO 11 PUBLICITARIA SRL';

-- LMB S.A. - 22,467,000 Gs (14 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1119, 'LMB S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1119 
WHERE cliente_original = 'LMB S.A.';

-- FRUTIKA SRL - 21,800,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1120, 'FRUTIKA SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1120 
WHERE cliente_original = 'FRUTIKA SRL';

-- ROW COMMS E.A.S - 21,500,000 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1121, 'ROW COMMS E.A.S');
UPDATE fact_facturacion 
SET anunciante_id = 1121 
WHERE cliente_original = 'ROW COMMS E.A.S';

-- FOCUS TECHNOLOGY S.A - 21,488,327 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1122, 'FOCUS TECHNOLOGY S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1122 
WHERE cliente_original = 'FOCUS TECHNOLOGY S.A';

-- INDUSTRIAS CREATIVAS ON SAECA - 20,893,548 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1123, 'INDUSTRIAS CREATIVAS ON SAECA');
UPDATE fact_facturacion 
SET anunciante_id = 1123 
WHERE cliente_original = 'INDUSTRIAS CREATIVAS ON SAECA';

-- GIULIANA SACCARELLO - 19,212,295 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1124, 'GIULIANA SACCARELLO');
UPDATE fact_facturacion 
SET anunciante_id = 1124 
WHERE cliente_original = 'GIULIANA SACCARELLO';

-- COMERCIAL SAN CAYETANO S.R.L - 19,090,901 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1125, 'COMERCIAL SAN CAYETANO S.R.L');
UPDATE fact_facturacion 
SET anunciante_id = 1125 
WHERE cliente_original = 'COMERCIAL SAN CAYETANO S.R.L';

-- WILPAR SA - 18,142,935 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1126, 'WILPAR SA');
UPDATE fact_facturacion 
SET anunciante_id = 1126 
WHERE cliente_original = 'WILPAR SA';

-- BLACKLAND SA - 18,081,818 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1127, 'BLACKLAND SA');
UPDATE fact_facturacion 
SET anunciante_id = 1127 
WHERE cliente_original = 'BLACKLAND SA';

-- FERREVENTAS S.A. - 17,600,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1128, 'FERREVENTAS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1128 
WHERE cliente_original = 'FERREVENTAS S.A.';

-- DRUPILAND S.R.L - 17,448,715 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1129, 'DRUPILAND S.R.L');
UPDATE fact_facturacion 
SET anunciante_id = 1129 
WHERE cliente_original = 'DRUPILAND S.R.L';

-- FINANCIERA PARAGUAYO JAPONESA S.A.E.C.A. - 17,430,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1130, 'FINANCIERA PARAGUAYO JAPONESA S.A.E.C.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1130 
WHERE cliente_original = 'FINANCIERA PARAGUAYO JAPONESA S.A.E.C.A.';

-- ALISER SA - 16,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1131, 'ALISER SA');
UPDATE fact_facturacion 
SET anunciante_id = 1131 
WHERE cliente_original = 'ALISER SA';

-- OMPERFORMANCE PARAGUAY S.R.L. - 16,323,184 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1132, 'OMPERFORMANCE PARAGUAY S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1132 
WHERE cliente_original = 'OMPERFORMANCE PARAGUAY S.R.L.';

-- PAPIXCO SA - 16,200,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1133, 'PAPIXCO SA');
UPDATE fact_facturacion 
SET anunciante_id = 1133 
WHERE cliente_original = 'PAPIXCO SA';

-- GUATAPORA S.A. - 15,313,182 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1134, 'GUATAPORA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1134 
WHERE cliente_original = 'GUATAPORA S.A.';

-- SUNSET SA COMERCIAL INDUS. Y DE SERV. - 15,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1135, 'SUNSET SA COMERCIAL INDUS. Y DE SERV.');
UPDATE fact_facturacion 
SET anunciante_id = 1135 
WHERE cliente_original = 'SUNSET SA COMERCIAL INDUS. Y DE SERV.';

-- RG SA - 14,318,182 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1136, 'RG SA');
UPDATE fact_facturacion 
SET anunciante_id = 1136 
WHERE cliente_original = 'RG SA';

-- PLAN INTERNATIONAL INC. - 13,950,000 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1137, 'PLAN INTERNATIONAL INC.');
UPDATE fact_facturacion 
SET anunciante_id = 1137 
WHERE cliente_original = 'PLAN INTERNATIONAL INC.';

-- WYNWOOD SA - 13,929,300 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1138, 'WYNWOOD SA');
UPDATE fact_facturacion 
SET anunciante_id = 1138 
WHERE cliente_original = 'WYNWOOD SA';

-- UNIVERSIDAD PRIVADA MARIA SERRANA - 13,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1139, 'UNIVERSIDAD PRIVADA MARIA SERRANA');
UPDATE fact_facturacion 
SET anunciante_id = 1139 
WHERE cliente_original = 'UNIVERSIDAD PRIVADA MARIA SERRANA';

-- WILD FI HUB - 13,334,253 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1140, 'WILD FI HUB');
UPDATE fact_facturacion 
SET anunciante_id = 1140 
WHERE cliente_original = 'WILD FI HUB';

-- ESMART SRL - 13,200,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1141, 'ESMART SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1141 
WHERE cliente_original = 'ESMART SRL';

-- CINEMARK PARAGUAY S.R.L. - 12,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1142, 'CINEMARK PARAGUAY S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1142 
WHERE cliente_original = 'CINEMARK PARAGUAY S.R.L.';

-- KINGSPAN MV ACEROS SA - 12,350,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1143, 'KINGSPAN MV ACEROS SA');
UPDATE fact_facturacion 
SET anunciante_id = 1143 
WHERE cliente_original = 'KINGSPAN MV ACEROS SA';

-- FASA SA - 12,250,000 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1144, 'FASA SA');
UPDATE fact_facturacion 
SET anunciante_id = 1144 
WHERE cliente_original = 'FASA SA';

-- YA PUBLICIDAD S.A. - 12,150,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1145, 'YA PUBLICIDAD S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1145 
WHERE cliente_original = 'YA PUBLICIDAD S.A.';

-- JUAN NICOLAS ROMAN ROA - 12,060,953 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1146, 'JUAN NICOLAS ROMAN ROA');
UPDATE fact_facturacion 
SET anunciante_id = 1146 
WHERE cliente_original = 'JUAN NICOLAS ROMAN ROA';

-- ALEMAN PARAGUAYO CANADIENSE SA - 12,000,000 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1147, 'ALEMAN PARAGUAYO CANADIENSE SA');
UPDATE fact_facturacion 
SET anunciante_id = 1147 
WHERE cliente_original = 'ALEMAN PARAGUAYO CANADIENSE SA';

-- BIGGIE S.A. - 11,905,817 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1148, 'BIGGIE S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1148 
WHERE cliente_original = 'BIGGIE S.A.';

-- CENTRAL DE INTELIGENCIA EN MEDIOS S.A. - 11,504,925 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1149, 'CENTRAL DE INTELIGENCIA EN MEDIOS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1149 
WHERE cliente_original = 'CENTRAL DE INTELIGENCIA EN MEDIOS S.A.';

-- NORD S.A. - 11,454,545 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1150, 'NORD S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1150 
WHERE cliente_original = 'NORD S.A.';

-- GRUPO ROMA S.R.L - 11,400,000 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1151, 'GRUPO ROMA S.R.L');
UPDATE fact_facturacion 
SET anunciante_id = 1151 
WHERE cliente_original = 'GRUPO ROMA S.R.L';

-- UNIVERSIDAD DEL CONO SUR DE LAS AMERICAS - 11,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1152, 'UNIVERSIDAD DEL CONO SUR DE LAS AMERICAS');
UPDATE fact_facturacion 
SET anunciante_id = 1152 
WHERE cliente_original = 'UNIVERSIDAD DEL CONO SUR DE LAS AMERICAS';

-- JOHNSON & JOHNSON DEL PARAGUAY SA - 10,990,910 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1153, 'JOHNSON & JOHNSON DEL PARAGUAY SA');
UPDATE fact_facturacion 
SET anunciante_id = 1153 
WHERE cliente_original = 'JOHNSON & JOHNSON DEL PARAGUAY SA';

-- IBRA IMPORT S.R.L - 10,960,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1154, 'IBRA IMPORT S.R.L');
UPDATE fact_facturacion 
SET anunciante_id = 1154 
WHERE cliente_original = 'IBRA IMPORT S.R.L';

-- B&A TRADING SOCIEDAD ANÓNIMA - 10,363,650 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1155, 'B&A TRADING SOCIEDAD ANÓNIMA');
UPDATE fact_facturacion 
SET anunciante_id = 1155 
WHERE cliente_original = 'B&A TRADING SOCIEDAD ANÓNIMA';

-- BIC S.A - 10,328,000 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1156, 'BIC S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1156 
WHERE cliente_original = 'BIC S.A';

-- FULMI SA - 10,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1157, 'FULMI SA');
UPDATE fact_facturacion 
SET anunciante_id = 1157 
WHERE cliente_original = 'FULMI SA';

-- DOCUMENTA S.A. - 10,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1158, 'DOCUMENTA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1158 
WHERE cliente_original = 'DOCUMENTA S.A.';

-- ELECTRO DIESEL SA - 9,280,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1159, 'ELECTRO DIESEL SA');
UPDATE fact_facturacion 
SET anunciante_id = 1159 
WHERE cliente_original = 'ELECTRO DIESEL SA';

-- CAMPING 44 S.A. - 9,100,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1160, 'CAMPING 44 S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1160 
WHERE cliente_original = 'CAMPING 44 S.A.';

-- MULAIR SA - 9,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1161, 'MULAIR SA');
UPDATE fact_facturacion 
SET anunciante_id = 1161 
WHERE cliente_original = 'MULAIR SA';

-- ALTAMIRA GROUP SA - 9,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1162, 'ALTAMIRA GROUP SA');
UPDATE fact_facturacion 
SET anunciante_id = 1162 
WHERE cliente_original = 'ALTAMIRA GROUP SA';

-- HANACE SACI - 9,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1163, 'HANACE SACI');
UPDATE fact_facturacion 
SET anunciante_id = 1163 
WHERE cliente_original = 'HANACE SACI';

-- PROFITAL SA - 8,400,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1164, 'PROFITAL SA');
UPDATE fact_facturacion 
SET anunciante_id = 1164 
WHERE cliente_original = 'PROFITAL SA';

-- RODRIGUEZ HNOS. SAECA - 8,149,705 Gs (9 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1165, 'RODRIGUEZ HNOS. SAECA');
UPDATE fact_facturacion 
SET anunciante_id = 1165 
WHERE cliente_original = 'RODRIGUEZ HNOS. SAECA';

-- RODRIGUEZ HNOS S.R.L. - 8,100,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1166, 'RODRIGUEZ HNOS S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1166 
WHERE cliente_original = 'RODRIGUEZ HNOS S.R.L.';

-- RODRIGUEZ HNOS. S.A.E.C.A. - 8,100,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1167, 'RODRIGUEZ HNOS. S.A.E.C.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1167 
WHERE cliente_original = 'RODRIGUEZ HNOS. S.A.E.C.A.';

-- RUVAL SA - 8,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1168, 'RUVAL SA');
UPDATE fact_facturacion 
SET anunciante_id = 1168 
WHERE cliente_original = 'RUVAL SA';

-- LOOK UP SA - 7,896,120 Gs (10 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1169, 'LOOK UP SA');
UPDATE fact_facturacion 
SET anunciante_id = 1169 
WHERE cliente_original = 'LOOK UP SA';

-- HEY NETWORK S.A. - 7,773,625 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1170, 'HEY NETWORK S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1170 
WHERE cliente_original = 'HEY NETWORK S.A.';

-- MATHER COMPANY SRL - 7,200,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1171, 'MATHER COMPANY SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1171 
WHERE cliente_original = 'MATHER COMPANY SRL';

-- AGROINDUSTRIAL SELENT SA - 7,090,900 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1172, 'AGROINDUSTRIAL SELENT SA');
UPDATE fact_facturacion 
SET anunciante_id = 1172 
WHERE cliente_original = 'AGROINDUSTRIAL SELENT SA';

-- STEPHANIE MONTSERRAT KUNZLE DUARTE - 7,071,136 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1173, 'STEPHANIE MONTSERRAT KUNZLE DUARTE');
UPDATE fact_facturacion 
SET anunciante_id = 1173 
WHERE cliente_original = 'STEPHANIE MONTSERRAT KUNZLE DUARTE';

-- DECIMAL  S.R.L. - 6,909,091 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1174, 'DECIMAL  S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1174 
WHERE cliente_original = 'DECIMAL  S.R.L.';

-- OJO DE PEZ S.A. - 6,900,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1175, 'OJO DE PEZ S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1175 
WHERE cliente_original = 'OJO DE PEZ S.A.';

-- CAJA MUTUAL DE COOPERATIVISTAS DEL PARAGUAY - 6,776,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1176, 'CAJA MUTUAL DE COOPERATIVISTAS DEL PARAGUAY');
UPDATE fact_facturacion 
SET anunciante_id = 1176 
WHERE cliente_original = 'CAJA MUTUAL DE COOPERATIVISTAS DEL PARAGUAY';

-- AMARAL & ASOCIADOS - 6,599,650 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1177, 'AMARAL & ASOCIADOS');
UPDATE fact_facturacion 
SET anunciante_id = 1177 
WHERE cliente_original = 'AMARAL & ASOCIADOS';

-- E.E.M.A SA - 6,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1178, 'E.E.M.A SA');
UPDATE fact_facturacion 
SET anunciante_id = 1178 
WHERE cliente_original = 'E.E.M.A SA';

-- BANCO PARA LA C. Y LA PRODUCCIÓN S.A. - 6,160,000 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1179, 'BANCO PARA LA C. Y LA PRODUCCIÓN S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1179 
WHERE cliente_original = 'BANCO PARA LA C. Y LA PRODUCCIÓN S.A.';

-- LOS LAGOS RESORT HOTEL SA - 6,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1180, 'LOS LAGOS RESORT HOTEL SA');
UPDATE fact_facturacion 
SET anunciante_id = 1180 
WHERE cliente_original = 'LOS LAGOS RESORT HOTEL SA';

-- EMILIO FEDERICO HERMOSILLA SILVA - 6,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1181, 'EMILIO FEDERICO HERMOSILLA SILVA');
UPDATE fact_facturacion 
SET anunciante_id = 1181 
WHERE cliente_original = 'EMILIO FEDERICO HERMOSILLA SILVA';

-- PRODUCTORA X SA - 6,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1182, 'PRODUCTORA X SA');
UPDATE fact_facturacion 
SET anunciante_id = 1182 
WHERE cliente_original = 'PRODUCTORA X SA';

-- INMOBILIARIA DEL ESTE S.A. - 5,636,364 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1183, 'INMOBILIARIA DEL ESTE S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1183 
WHERE cliente_original = 'INMOBILIARIA DEL ESTE S.A.';

-- KEMSA CISA - 5,484,818 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1184, 'KEMSA CISA');
UPDATE fact_facturacion 
SET anunciante_id = 1184 
WHERE cliente_original = 'KEMSA CISA';

-- SUPLIMAR SRL - 5,454,545 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1185, 'SUPLIMAR SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1185 
WHERE cliente_original = 'SUPLIMAR SRL';

-- LEANDRO MARTINEZ - 5,099,976 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1186, 'LEANDRO MARTINEZ');
UPDATE fact_facturacion 
SET anunciante_id = 1186 
WHERE cliente_original = 'LEANDRO MARTINEZ';

-- RADIO ÑANDUTI SA - 5,000,000 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1187, 'RADIO ÑANDUTI SA');
UPDATE fact_facturacion 
SET anunciante_id = 1187 
WHERE cliente_original = 'RADIO ÑANDUTI SA';

-- PARAISO SA DE SERVICIOS GENERALES - 5,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1188, 'PARAISO SA DE SERVICIOS GENERALES');
UPDATE fact_facturacion 
SET anunciante_id = 1188 
WHERE cliente_original = 'PARAISO SA DE SERVICIOS GENERALES';

-- FERNANDO DE LA MORA S.A. - 4,968,225 Gs (11 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1189, 'FERNANDO DE LA MORA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1189 
WHERE cliente_original = 'FERNANDO DE LA MORA S.A.';

-- LOGO SRL - 4,909,091 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1190, 'LOGO SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1190 
WHERE cliente_original = 'LOGO SRL';

-- HUAWEI TECHNOLOGIES PARAGUAY S.A. - 4,816,480 Gs (8 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1191, 'HUAWEI TECHNOLOGIES PARAGUAY S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1191 
WHERE cliente_original = 'HUAWEI TECHNOLOGIES PARAGUAY S.A.';

-- TELEVISORA DEL ESTE S.A. - 4,724,144 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1192, 'TELEVISORA DEL ESTE S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1192 
WHERE cliente_original = 'TELEVISORA DEL ESTE S.A.';

-- OSCAR ROJAS MORA - 4,599,935 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1193, 'OSCAR ROJAS MORA');
UPDATE fact_facturacion 
SET anunciante_id = 1193 
WHERE cliente_original = 'OSCAR ROJAS MORA';

-- CARMEN DÍAZ - 4,590,910 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1194, 'CARMEN DÍAZ');
UPDATE fact_facturacion 
SET anunciante_id = 1194 
WHERE cliente_original = 'CARMEN DÍAZ';

-- CAMIPAR S.R.L. - 4,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1195, 'CAMIPAR S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1195 
WHERE cliente_original = 'CAMIPAR S.R.L.';

-- FERNANDO SEBASTIAN LEIVA GONZALEZ - 4,389,091 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1196, 'FERNANDO SEBASTIAN LEIVA GONZALEZ');
UPDATE fact_facturacion 
SET anunciante_id = 1196 
WHERE cliente_original = 'FERNANDO SEBASTIAN LEIVA GONZALEZ';

-- 1º DE MARZO S.A. - 4,388,571 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1197, '1º DE MARZO S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1197 
WHERE cliente_original = '1º DE MARZO S.A.';

-- BNB INVEST CASA DE BOLSA S.A. - 4,313,650 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1198, 'BNB INVEST CASA DE BOLSA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1198 
WHERE cliente_original = 'BNB INVEST CASA DE BOLSA S.A.';

-- A.R.P FRECUENCIA MODULAR S.R.L - 4,251,086 Gs (7 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1199, 'A.R.P FRECUENCIA MODULAR S.R.L');
UPDATE fact_facturacion 
SET anunciante_id = 1199 
WHERE cliente_original = 'A.R.P FRECUENCIA MODULAR S.R.L';

-- RIO SEGUROS S.A. - 4,232,999 Gs (22 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1200, 'RIO SEGUROS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1200 
WHERE cliente_original = 'RIO SEGUROS S.A.';

-- MERCEDES MARIA TERESA ENCINA GAONA - 4,045,455 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1201, 'MERCEDES MARIA TERESA ENCINA GAONA');
UPDATE fact_facturacion 
SET anunciante_id = 1201 
WHERE cliente_original = 'MERCEDES MARIA TERESA ENCINA GAONA';

-- RODOLFO MAX FRIEDMANN ORTIGOZA - 4,000,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1202, 'RODOLFO MAX FRIEDMANN ORTIGOZA');
UPDATE fact_facturacion 
SET anunciante_id = 1202 
WHERE cliente_original = 'RODOLFO MAX FRIEDMANN ORTIGOZA';

-- B.C. S.R.L. - 3,885,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1203, 'B.C. S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1203 
WHERE cliente_original = 'B.C. S.R.L.';

-- NIMABO S.A. - 3,873,962 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1204, 'NIMABO S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1204 
WHERE cliente_original = 'NIMABO S.A.';

-- OPY PARAGUAY E.A.S. UNIPERSONAL - 3,636,364 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1205, 'OPY PARAGUAY E.A.S. UNIPERSONAL');
UPDATE fact_facturacion 
SET anunciante_id = 1205 
WHERE cliente_original = 'OPY PARAGUAY E.A.S. UNIPERSONAL';

-- UNIVERSIDAD AUTONOMA SAN SEBASTIAN - 3,600,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1206, 'UNIVERSIDAD AUTONOMA SAN SEBASTIAN');
UPDATE fact_facturacion 
SET anunciante_id = 1206 
WHERE cliente_original = 'UNIVERSIDAD AUTONOMA SAN SEBASTIAN';

-- FOODCO SA - 3,600,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1207, 'FOODCO SA');
UPDATE fact_facturacion 
SET anunciante_id = 1207 
WHERE cliente_original = 'FOODCO SA';

-- CLÍNICA VETERINARIA BIBOLINI E.A.S. - 3,600,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1208, 'CLÍNICA VETERINARIA BIBOLINI E.A.S.');
UPDATE fact_facturacion 
SET anunciante_id = 1208 
WHERE cliente_original = 'CLÍNICA VETERINARIA BIBOLINI E.A.S.';

-- GRUPO VIERCI - 3,586,036 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1209, 'GRUPO VIERCI');
UPDATE fact_facturacion 
SET anunciante_id = 1209 
WHERE cliente_original = 'GRUPO VIERCI';

-- TATAKUA ALIMENTOS SA - 3,363,636 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1210, 'TATAKUA ALIMENTOS SA');
UPDATE fact_facturacion 
SET anunciante_id = 1210 
WHERE cliente_original = 'TATAKUA ALIMENTOS SA';

-- GLOBAL MEDIA GROUP S.R.L. - 3,150,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1211, 'GLOBAL MEDIA GROUP S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1211 
WHERE cliente_original = 'GLOBAL MEDIA GROUP S.R.L.';

-- BLOOM WELLNESS CENTER & SPA E.A.S. - 2,900,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1212, 'BLOOM WELLNESS CENTER & SPA E.A.S.');
UPDATE fact_facturacion 
SET anunciante_id = 1212 
WHERE cliente_original = 'BLOOM WELLNESS CENTER & SPA E.A.S.';

-- H3 AGROCHEMICALS" SOCIEDAD ANONIMA - 2,791,249 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1213, 'H3 AGROCHEMICALS" SOCIEDAD ANONIMA');
UPDATE fact_facturacion 
SET anunciante_id = 1213 
WHERE cliente_original = 'H3 AGROCHEMICALS" SOCIEDAD ANONIMA';

-- FEME S.A. - 2,692,768 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1214, 'FEME S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1214 
WHERE cliente_original = 'FEME S.A.';

-- TRADIMEX SRL - 2,550,000 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1215, 'TRADIMEX SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1215 
WHERE cliente_original = 'TRADIMEX SRL';

-- UNIVERSIDAD CENTRO MEDICO BAUTISTA - 2,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1216, 'UNIVERSIDAD CENTRO MEDICO BAUTISTA');
UPDATE fact_facturacion 
SET anunciante_id = 1216 
WHERE cliente_original = 'UNIVERSIDAD CENTRO MEDICO BAUTISTA';

-- CONSORCIO TIV - 2,500,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1217, 'CONSORCIO TIV');
UPDATE fact_facturacion 
SET anunciante_id = 1217 
WHERE cliente_original = 'CONSORCIO TIV';

-- FERNANDO BENÍTEZ - 2,450,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1218, 'FERNANDO BENÍTEZ');
UPDATE fact_facturacion 
SET anunciante_id = 1218 
WHERE cliente_original = 'FERNANDO BENÍTEZ';

-- BLU-TRADE S.A. - 2,437,500 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1219, 'BLU-TRADE S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1219 
WHERE cliente_original = 'BLU-TRADE S.A.';

-- FUNDACION TEXO PARA EL ARTE CONTEMPORANEO - 2,401,898 Gs (15 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1220, 'FUNDACION TEXO PARA EL ARTE CONTEMPORANEO');
UPDATE fact_facturacion 
SET anunciante_id = 1220 
WHERE cliente_original = 'FUNDACION TEXO PARA EL ARTE CONTEMPORANEO';

-- A TODO PULMÓN PARAGUAY RESPIRA - 2,250,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1221, 'A TODO PULMÓN PARAGUAY RESPIRA');
UPDATE fact_facturacion 
SET anunciante_id = 1221 
WHERE cliente_original = 'A TODO PULMÓN PARAGUAY RESPIRA';

-- GRUPO FOCUS - 2,183,879 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1222, 'GRUPO FOCUS');
UPDATE fact_facturacion 
SET anunciante_id = 1222 
WHERE cliente_original = 'GRUPO FOCUS';

-- MULTIMEDIA S.A - 2,181,817 Gs (7 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1223, 'MULTIMEDIA S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1223 
WHERE cliente_original = 'MULTIMEDIA S.A';

-- PALERMO S.A. - 1,931,820 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1224, 'PALERMO S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1224 
WHERE cliente_original = 'PALERMO S.A.';

-- RADIO ÑEMBY SRL - 1,900,493 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1225, 'RADIO ÑEMBY SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1225 
WHERE cliente_original = 'RADIO ÑEMBY SRL';

-- COSAFI S.A - 1,850,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1226, 'COSAFI S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1226 
WHERE cliente_original = 'COSAFI S.A';

-- ECOBRAND SRL - 1,800,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1227, 'ECOBRAND SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1227 
WHERE cliente_original = 'ECOBRAND SRL';

-- ALMIRIA DEL PADRE NUÑEZ - 1,750,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1228, 'ALMIRIA DEL PADRE NUÑEZ');
UPDATE fact_facturacion 
SET anunciante_id = 1228 
WHERE cliente_original = 'ALMIRIA DEL PADRE NUÑEZ';

-- JULIO BRITEZ - 1,620,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1229, 'JULIO BRITEZ');
UPDATE fact_facturacion 
SET anunciante_id = 1229 
WHERE cliente_original = 'JULIO BRITEZ';

-- PRESTAMATIC S.R.L. - 1,454,545 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1230, 'PRESTAMATIC S.R.L.');
UPDATE fact_facturacion 
SET anunciante_id = 1230 
WHERE cliente_original = 'PRESTAMATIC S.R.L.';

-- IDEAS ENORMES SRL - 1,414,000 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1231, 'IDEAS ENORMES SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1231 
WHERE cliente_original = 'IDEAS ENORMES SRL';

-- METATRON S.A. - 1,400,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1232, 'METATRON S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1232 
WHERE cliente_original = 'METATRON S.A.';

-- MATIAS JOSE SANCHEZ PATRI - 1,332,076 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1233, 'MATIAS JOSE SANCHEZ PATRI');
UPDATE fact_facturacion 
SET anunciante_id = 1233 
WHERE cliente_original = 'MATIAS JOSE SANCHEZ PATRI';

-- CELESTE ANGULO - 1,016,817 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1234, 'CELESTE ANGULO');
UPDATE fact_facturacion 
SET anunciante_id = 1234 
WHERE cliente_original = 'CELESTE ANGULO';

-- NIMABO S.A - 1,005,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1235, 'NIMABO S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1235 
WHERE cliente_original = 'NIMABO S.A';

-- RUNNING TIME SRL - 909,091 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1236, 'RUNNING TIME SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1236 
WHERE cliente_original = 'RUNNING TIME SRL';

-- CARLOS ERNESTO DUARTE ZOELLNER - 909,091 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1237, 'CARLOS ERNESTO DUARTE ZOELLNER');
UPDATE fact_facturacion 
SET anunciante_id = 1237 
WHERE cliente_original = 'CARLOS ERNESTO DUARTE ZOELLNER';

-- CENTRAL DE VENTAS TV S.A. - 839,800 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1238, 'CENTRAL DE VENTAS TV S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1238 
WHERE cliente_original = 'CENTRAL DE VENTAS TV S.A.';

-- GUIDO CORONEL - 800,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1239, 'GUIDO CORONEL');
UPDATE fact_facturacion 
SET anunciante_id = 1239 
WHERE cliente_original = 'GUIDO CORONEL';

-- NILCOS SRL - 772,727 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1240, 'NILCOS SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1240 
WHERE cliente_original = 'NILCOS SRL';

-- LAKMI S.A - 727,273 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1241, 'LAKMI S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1241 
WHERE cliente_original = 'LAKMI S.A';

-- DARIO CARDONA HERREROS - 715,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1242, 'DARIO CARDONA HERREROS');
UPDATE fact_facturacion 
SET anunciante_id = 1242 
WHERE cliente_original = 'DARIO CARDONA HERREROS';

-- IVAN BURIFALDI - 699,996 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1243, 'IVAN BURIFALDI');
UPDATE fact_facturacion 
SET anunciante_id = 1243 
WHERE cliente_original = 'IVAN BURIFALDI';

-- CARTONES YAGUARETE S.A. - 663,636 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1244, 'CARTONES YAGUARETE S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1244 
WHERE cliente_original = 'CARTONES YAGUARETE S.A.';

-- VENUS COMUNICACIONES S.A. - 545,455 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1245, 'VENUS COMUNICACIONES S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1245 
WHERE cliente_original = 'VENUS COMUNICACIONES S.A.';

-- YESSICA GONZÁLEZ - 523,638 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1246, 'YESSICA GONZÁLEZ');
UPDATE fact_facturacion 
SET anunciante_id = 1246 
WHERE cliente_original = 'YESSICA GONZÁLEZ';

-- EXTERIOR I.P.S.A. - 516,600 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1247, 'EXTERIOR I.P.S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1247 
WHERE cliente_original = 'EXTERIOR I.P.S.A.';

-- EDUARDO DANIEL NUÑEZ - 480,000 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1248, 'EDUARDO DANIEL NUÑEZ');
UPDATE fact_facturacion 
SET anunciante_id = 1248 
WHERE cliente_original = 'EDUARDO DANIEL NUÑEZ';

-- LCI E.A.S. - 445,455 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1249, 'LCI E.A.S.');
UPDATE fact_facturacion 
SET anunciante_id = 1249 
WHERE cliente_original = 'LCI E.A.S.';

-- JACQUELINE YANE RAMIREZ CABRAL - 385,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1250, 'JACQUELINE YANE RAMIREZ CABRAL');
UPDATE fact_facturacion 
SET anunciante_id = 1250 
WHERE cliente_original = 'JACQUELINE YANE RAMIREZ CABRAL';

-- PEDRO FLORENTIN DEMESTRI - 385,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1251, 'PEDRO FLORENTIN DEMESTRI');
UPDATE fact_facturacion 
SET anunciante_id = 1251 
WHERE cliente_original = 'PEDRO FLORENTIN DEMESTRI';

-- JUAN CARLOS HRISUK KLEKOC - 384,413 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1252, 'JUAN CARLOS HRISUK KLEKOC');
UPDATE fact_facturacion 
SET anunciante_id = 1252 
WHERE cliente_original = 'JUAN CARLOS HRISUK KLEKOC';

-- LAURA MARTÍNEZ - 370,584 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1253, 'LAURA MARTÍNEZ');
UPDATE fact_facturacion 
SET anunciante_id = 1253 
WHERE cliente_original = 'LAURA MARTÍNEZ';

-- SELTZ S.A. - 363,636 Gs (6 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1254, 'SELTZ S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1254 
WHERE cliente_original = 'SELTZ S.A.';

-- LETICIA GARCIA - 272,727 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1255, 'LETICIA GARCIA');
UPDATE fact_facturacion 
SET anunciante_id = 1255 
WHERE cliente_original = 'LETICIA GARCIA';

-- ROBERTO EULOGIO CACERES - 270,000 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1256, 'ROBERTO EULOGIO CACERES');
UPDATE fact_facturacion 
SET anunciante_id = 1256 
WHERE cliente_original = 'ROBERTO EULOGIO CACERES';

-- SBB S.A. - 255,958 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1257, 'SBB S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1257 
WHERE cliente_original = 'SBB S.A.';

-- AMMUS S.A. - 231,819 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1258, 'AMMUS S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1258 
WHERE cliente_original = 'AMMUS S.A.';

-- E-360 PUBLICIDAD E.A.S. UNIPERSONAL - 231,818 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1259, 'E-360 PUBLICIDAD E.A.S. UNIPERSONAL');
UPDATE fact_facturacion 
SET anunciante_id = 1259 
WHERE cliente_original = 'E-360 PUBLICIDAD E.A.S. UNIPERSONAL';

-- MARIA JOSE OVIEDO - 135,455 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1260, 'MARIA JOSE OVIEDO');
UPDATE fact_facturacion 
SET anunciante_id = 1260 
WHERE cliente_original = 'MARIA JOSE OVIEDO';

-- MARIANO SANTAMARINA - 135,455 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1261, 'MARIANO SANTAMARINA');
UPDATE fact_facturacion 
SET anunciante_id = 1261 
WHERE cliente_original = 'MARIANO SANTAMARINA';

-- HECTOR FABIAN OVIEDO ACHUCARRO - 135,455 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1262, 'HECTOR FABIAN OVIEDO ACHUCARRO');
UPDATE fact_facturacion 
SET anunciante_id = 1262 
WHERE cliente_original = 'HECTOR FABIAN OVIEDO ACHUCARRO';

-- FABRIZIO HUG DE BELMONT VERA - 135,455 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1263, 'FABRIZIO HUG DE BELMONT VERA');
UPDATE fact_facturacion 
SET anunciante_id = 1263 
WHERE cliente_original = 'FABRIZIO HUG DE BELMONT VERA';

-- INTRADE S.A. - 109,090 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1264, 'INTRADE S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1264 
WHERE cliente_original = 'INTRADE S.A.';

-- CAFSA S.A. - 0 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1265, 'CAFSA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1265 
WHERE cliente_original = 'CAFSA S.A.';

-- DISCOVER PARAGUAY SA - 0 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1266, 'DISCOVER PARAGUAY SA');
UPDATE fact_facturacion 
SET anunciante_id = 1266 
WHERE cliente_original = 'DISCOVER PARAGUAY SA';

-- GRUPO NACIÓN - 0 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1267, 'GRUPO NACIÓN');
UPDATE fact_facturacion 
SET anunciante_id = 1267 
WHERE cliente_original = 'GRUPO NACIÓN';

-- PRO MARKETING SRL - 0 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1268, 'PRO MARKETING SRL');
UPDATE fact_facturacion 
SET anunciante_id = 1268 
WHERE cliente_original = 'PRO MARKETING SRL';

-- FAMILIAR CASA DE BOLSA S.A - 0 Gs (10 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1269, 'FAMILIAR CASA DE BOLSA S.A');
UPDATE fact_facturacion 
SET anunciante_id = 1269 
WHERE cliente_original = 'FAMILIAR CASA DE BOLSA S.A';

-- ROSA ORTIZ - 0 Gs (3 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1270, 'ROSA ORTIZ');
UPDATE fact_facturacion 
SET anunciante_id = 1270 
WHERE cliente_original = 'ROSA ORTIZ';

-- TELEDEPORTES PARAGUAY S.A. - 0 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1271, 'TELEDEPORTES PARAGUAY S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1271 
WHERE cliente_original = 'TELEDEPORTES PARAGUAY S.A.';

-- CISNEROS INTERACTIVE S.A. - 0 Gs (2 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1272, 'CISNEROS INTERACTIVE S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1272 
WHERE cliente_original = 'CISNEROS INTERACTIVE S.A.';

-- HUAWEI DEVICE (HONG KONG) CO., LIMITED - -222,424 Gs (8 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1273, 'HUAWEI DEVICE (HONG KONG) CO., LIMITED');
UPDATE fact_facturacion 
SET anunciante_id = 1273 
WHERE cliente_original = 'HUAWEI DEVICE (HONG KONG) CO., LIMITED';

-- CABAL PARAGUAY LTDA. - -1,455,454 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1274, 'CABAL PARAGUAY LTDA.');
UPDATE fact_facturacion 
SET anunciante_id = 1274 
WHERE cliente_original = 'CABAL PARAGUAY LTDA.';

-- TIGO SPORTS - -2,624,378 Gs (5 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1275, 'TIGO SPORTS');
UPDATE fact_facturacion 
SET anunciante_id = 1275 
WHERE cliente_original = 'TIGO SPORTS';

-- ARRONTI SA - -3,318,182 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1276, 'ARRONTI SA');
UPDATE fact_facturacion 
SET anunciante_id = 1276 
WHERE cliente_original = 'ARRONTI SA';

-- BRICK S.A.- TIGO SPORT TD - -4,582,863 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1277, 'BRICK S.A.- TIGO SPORT TD');
UPDATE fact_facturacion 
SET anunciante_id = 1277 
WHERE cliente_original = 'BRICK S.A.- TIGO SPORT TD';

-- PENTA S.A. - -5,080,000 Gs (7 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1278, 'PENTA S.A.');
UPDATE fact_facturacion 
SET anunciante_id = 1278 
WHERE cliente_original = 'PENTA S.A.';

-- SOLUTIONS 2 GO LATAM INC. - -6,014,224 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1279, 'SOLUTIONS 2 GO LATAM INC.');
UPDATE fact_facturacion 
SET anunciante_id = 1279 
WHERE cliente_original = 'SOLUTIONS 2 GO LATAM INC.';

-- CONSORCIO DL - -10,391,680 Gs (4 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1280, 'CONSORCIO DL');
UPDATE fact_facturacion 
SET anunciante_id = 1280 
WHERE cliente_original = 'CONSORCIO DL';

-- INDUSTRIA NACIONAL DEL CEMENTO - -14,827,273 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1281, 'INDUSTRIA NACIONAL DEL CEMENTO');
UPDATE fact_facturacion 
SET anunciante_id = 1281 
WHERE cliente_original = 'INDUSTRIA NACIONAL DEL CEMENTO';

-- MEGA AMERICA SA - -29,739,133 Gs (1 registros)
INSERT INTO dim_anunciante_perfil (anunciante_id, nombre_anunciante) 
VALUES (1282, 'MEGA AMERICA SA');
UPDATE fact_facturacion 
SET anunciante_id = 1282 
WHERE cliente_original = 'MEGA AMERICA SA';

