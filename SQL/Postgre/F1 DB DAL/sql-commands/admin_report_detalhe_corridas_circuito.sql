-- Relatório Admin (Parte 4/4): Detalha as corridas por circuito, mostrando o vencedor (PositionOrder=1), voltas e tempo total.
SET search_path TO "Grupo10";
SELECT
    CI.Name AS "Circuito",
    R.Name AS "Nome da Corrida",
    R.YEAR AS "Ano",
    RES.Laps AS "Voltas",
    RES.Time AS "Tempo Total"
FROM Races R
JOIN Circuits CI ON R.CircuitId = CI.CircuitId
JOIN Results RES ON R.RaceId = RES.RaceId
WHERE RES.PositionOrder = 1
ORDER BY CI.Name, R.YEAR, R.Round;