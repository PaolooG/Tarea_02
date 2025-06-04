-- Cargar el archivo CSV limpio
eventos = LOAD 'data/eventos_filtrados.csv' 
    USING PigStorage(',') 
    AS (tipo:chararray, ubicacion:chararray, timestamp:chararray, comuna:chararray);

-- Contar cantidad de eventos por tipo
por_tipo = GROUP eventos BY tipo;
conteo_por_tipo = FOREACH por_tipo GENERATE group AS tipo, COUNT(eventos) AS cantidad;

-- Contar cantidad de eventos por comuna
por_comuna = GROUP eventos BY comuna;
conteo_por_comuna = FOREACH por_comuna GENERATE group AS comuna, COUNT(eventos) AS cantidad;

-- Contar eventos por día (extraemos solo la fecha del timestamp)
eventos_con_fecha = FOREACH eventos GENERATE tipo, comuna, SUBSTRING(timestamp, 0, 10) AS fecha;
por_fecha = GROUP eventos_con_fecha BY fecha;
conteo_por_fecha = FOREACH por_fecha GENERATE group AS fecha, COUNT(eventos_con_fecha) AS cantidad;

-- Guardar los resultados
STORE conteo_por_tipo INTO 'output/conteo_por_tipo' USING PigStorage(',');
STORE conteo_por_comuna INTO 'output/conteo_por_comuna' USING PigStorage(',');
STORE conteo_por_fecha INTO 'output/conteo_por_fecha' USING PigStorage(',');
