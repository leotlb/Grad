-- Carrega os valores de DriverCount e ConstructorCount da tabela ID_Counts
-- para inicializar os contadores de ID na aplicação.
SET search_path TO "Grupo10";
SELECT DriverCount, ConstructorCount FROM ID_Counts LIMIT 1;