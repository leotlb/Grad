SET search_path TO "Grupo10";

-- Índice para joins com a tabela Races
CREATE INDEX idx_results_raceid ON Results (RaceId);

-- Índice para filtros e joins por piloto
CREATE INDEX idx_results_driverid ON Results (DriverId);

-- Índice para filtros e joins por escuderia
CREATE INDEX idx_results_constructorid ON Results (ConstructorId);

-- Índice para joins com a tabela Status
CREATE INDEX idx_results_statusid ON Results (StatusId);

--Índice para Consultas por Ano
CREATE INDEX idx_races_year ON Races (Year);