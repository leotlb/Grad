-- Busca as corridas do ano corrente, incluindo nome, total de voltas e horário.
-- O total de voltas é o máximo registrado para cada corrida na tabela de resultados.
SET search_path TO "Grupo10";
SELECT
    RA.Name AS nomecorrida,
    MAX(RES.Laps) AS totalvoltas,
    RA.Time AS tempo
FROM Races AS RA
JOIN Results AS RES ON RA.RaceId = RES.RaceId
WHERE RA.YEAR = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY RA.RaceId, RA.Name, RA.Time, RA.Date
ORDER BY RA.Date;