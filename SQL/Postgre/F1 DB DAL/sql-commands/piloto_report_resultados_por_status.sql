-- Relatório Piloto: Conta a quantidade de resultados de corrida para cada status final, filtrado pelo piloto logado.
SELECT
    S.Status AS "Status",
    COUNT(R.StatusId) AS "Quantidade"
FROM Results R
JOIN Status S ON R.StatusId = S.StatusId
WHERE R.DriverId = %s
GROUP BY S.StatusId, S.Status
ORDER BY "Quantidade" DESC;