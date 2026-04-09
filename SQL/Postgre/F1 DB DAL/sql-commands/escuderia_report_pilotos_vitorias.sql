-- Relatório Escuderia: Lista todos os pilotos que correram pela escuderia e sua respectiva quantidade de vitórias.
-- Ordena por número de vitórias (decrescente) e depois por nome.
SELECT
    D.Forename || ' ' || D.Surname AS "Nome Completo do Piloto",
    COUNT(CASE WHEN RES.Position = 1 THEN 1 END) AS "Quantidade de Vitórias"
FROM Driver D
JOIN Results RES ON D.DriverId = RES.DriverId
WHERE RES.ConstructorId = %s
GROUP BY D.DriverId, "Nome Completo do Piloto"
ORDER BY "Quantidade de Vitórias" DESC, "Nome Completo do Piloto";