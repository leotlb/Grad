-- Lista as escuderias e a soma de seus pontos no ano corrente.
-- Agrupa os resultados por escuderia e ordena por total de pontos.
SET search_path TO "Grupo10";
SELECT
    C.Name AS nomeescuderia,
    SUM(R.Points) AS totalpontos
FROM Results AS R
JOIN Constructors AS C ON R.ConstructorId = C.ConstructorId
JOIN Races AS RA ON R.RaceId = RA.RaceId
WHERE RA.YEAR = EXTRACT(YEAR FROM CURRENT_DATE) -- Usar CURRENT_DATE em produção
GROUP BY C.ConstructorId, C.Name
ORDER BY totalpontos DESC;