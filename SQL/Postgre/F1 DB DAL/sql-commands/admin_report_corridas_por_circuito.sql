-- Relatório Admin (Parte 3/4): Agrupa as corridas por circuito, mostrando quantidade, mínimo, média e máximo de voltas.
SET search_path TO "Grupo10";
WITH RaceLaps AS (
  SELECT RaceId, MAX(Laps) as num_laps
  FROM Results
  WHERE Laps > 0
  GROUP BY RaceId
)
SELECT
    C.Name AS "Circuito",
    COUNT(R.RaceId) AS "Qtd. Corridas",
    MIN(RL.num_laps) AS "Mín. Voltas",
    ROUND(AVG(RL.num_laps), 1) AS "Média Voltas",
    MAX(RL.num_laps) AS "Máx. Voltas"
FROM Races R
JOIN Circuits C ON R.CircuitId = C.CircuitId
JOIN RaceLaps RL ON R.RaceId = RL.RaceId
GROUP BY C.CircuitId, C.Name
ORDER BY C.Name;