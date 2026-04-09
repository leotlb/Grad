-- Busca contagens totais para o dashboard do administrador.
-- Utiliza subconsultas para contar pilotos, escuderias e temporadas distintas.
SET search_path TO "Grupo10";
SELECT
    (SELECT COUNT(*) FROM Driver) AS total_pilotos,
    (SELECT COUNT(*) FROM Constructors) AS total_escuderias,
    (SELECT COUNT(DISTINCT YEAR) FROM Races) AS total_temporadas;