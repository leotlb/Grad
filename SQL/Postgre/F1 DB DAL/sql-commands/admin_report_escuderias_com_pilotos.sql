-- Relatório Admin (Parte 1/4): Lista todas as escuderias e a quantidade de pilotos distintos que já correram por elas.
SET search_path TO "Grupo10";
SELECT C.Name AS "Nome da Escuderia", COUNT(DISTINCT RES.DriverId) AS "Qtd. Pilotos"
FROM Constructors C
LEFT JOIN Results RES ON C.ConstructorId = RES.ConstructorId
GROUP BY C.ConstructorId, C.Name ORDER BY C.Name;