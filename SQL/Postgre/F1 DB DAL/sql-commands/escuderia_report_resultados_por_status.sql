-- Relatório Escuderia: Conta a quantidade de resultados de corrida para cada status final, filtrado pela escuderia logada.
SELECT
    S.Status AS "Status",
    COUNT(R.StatusId) AS "Quantidade"
FROM Results R
JOIN Status S ON R.StatusId = S.StatusId
WHERE R.ConstructorId = %s
GROUP BY S.StatusId, S.Status
ORDER BY "Quantidade" DESC;