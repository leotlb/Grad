-- Lista os pilotos e a soma de seus pontos no ano corrente.
-- Agrupa os resultados por piloto e ordena por total de pontos.
SET search_path TO "Grupo10";
SELECT
    D.Forename || ' ' || D.Surname AS nomepiloto,
    SUM(R.Points) AS totalpontos
FROM Results AS R
JOIN Driver AS D ON R.DriverId = D.DriverId
JOIN Races AS RA ON R.RaceId = RA.RaceId
WHERE RA.YEAR = EXTRACT(YEAR FROM CURRENT_DATE) AND R.Points > 0
GROUP BY D.DriverId, D.Forename, D.Surname
ORDER BY totalpontos DESC;