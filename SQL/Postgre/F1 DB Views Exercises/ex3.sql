SET search_path TO "Grupo10";
--------------------------------------------------------------------------------------
--Ex 3

CREATE OR REPLACE VIEW Circuitos_completa AS
SELECT
    c.Name AS CircuitName,
    c.Location AS CircuitLocation,
    c.Country AS CircuitCountryName,
    co.Code AS CountryCode,
    co.Continent AS CountryContinent
FROM
    Circuits c
LEFT JOIN                          -- Seleciona todos os circuitos
    Countries co
ON
    c.Country = co.Name;           -- Condição de junção: Circuits.Country = Countries.Name

--Visão e count
/*

SELECT * FROM Circuitos_completa
LIMIT 10;

SELECT COUNT(*) AS TotalTuplas
FROM Circuitos_completa;

*/