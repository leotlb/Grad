-- Consulta de Escuderia: Busca pilotos pelo primeiro nome que correram pela escuderia logada.
-- A busca é case-insensitive (ILIKE) e retorna resultados distintos.
SET search_path TO "Grupo10";
SELECT DISTINCT
    D.Forename || ' ' || D.Surname AS "Nome Completo",
    TO_CHAR(D.Dob, 'DD/MM/YYYY') AS "Data de Nascimento",
    D.Nationality AS "Nacionalidade"
FROM Driver D
JOIN Results RES ON D.DriverId = RES.DriverId
WHERE RES.ConstructorId = %s AND D.Forename ILIKE %s;