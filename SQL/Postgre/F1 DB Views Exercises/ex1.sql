SET search_path TO "Grupo10";
--------------------------------------------------------------------------------------
--Ex 1

CREATE MATERIALIZED VIEW Aeroportos_Brasileiros AS
SELECT
    A.Name AS NomeAeroporto,
    A.LatDeg AS LatitudeAeroporto,
    A.LongDeg AS LongitudeAeroporto,
    GC.Name AS NomeCidade,
    GC.Population AS PopulacaoCidade,
    C.Name AS NomePais,
    C.Continent AS ContinentePais
FROM
    Airports A
JOIN
    Countries C ON A.ISOCountry = C.Code  -- Vincula aeroporto ao país
JOIN
    GeoCities15K GC ON A.City = GC.Name AND C.Code = GC.Country -- Vincula aeroporto à cidade DENTRO do mesmo país
WHERE
    C.Code = 'BR'; -- Filtra apenas para o Brasil (ISO Code 'BR')


-- Visão 
SELECT * FROM Aeroportos_Brasileiros
LIMIT 10;