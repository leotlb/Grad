-- Dashboard Piloto (3/3): Agrupa estatísticas do piloto (pontos, vitórias, corridas) por ano e por circuito.
SELECT
    RA.YEAR AS ano,
    C.Name AS nome_circuito,
    SUM(RES.Points) AS qtd_pontos,
    COUNT(CASE WHEN RES.Position = 1 THEN 1 END) AS qtd_vitorias,
    COUNT(RES.RaceId) AS qtd_corridas
FROM Results AS RES
JOIN Races AS RA ON RES.RaceId = RA.RaceId
JOIN Circuits AS C ON RA.CircuitId = C.CircuitId
WHERE RES.DriverId = %s
GROUP BY RA.YEAR, C.CircuitId, C.Name
ORDER BY RA.YEAR DESC, C.Name;