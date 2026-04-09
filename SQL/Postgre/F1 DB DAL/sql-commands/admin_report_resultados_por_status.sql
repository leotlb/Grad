-- Relatório Admin: Conta a quantidade de resultados de corrida para cada status final.
-- Agrupa por status e ordena pela quantidade em ordem decrescente.
SET search_path TO "Grupo10";
SELECT
    S.Status AS "Nome do Status",
    COUNT(R.StatusId) AS "Quantidade"
FROM Results R
JOIN Status S ON R.StatusId = S.StatusId
GROUP BY S.StatusId, S.Status
ORDER BY "Quantidade" DESC;