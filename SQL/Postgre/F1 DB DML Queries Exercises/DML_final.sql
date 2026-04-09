SET search_path TO "Grupo10";


-- Exercício 1
-- Apesar do enunciado sugerir a utilização da tabela Driverstandings para consulta, o valor da pontuação na tabela está acumulado ano a ano,
-- O que levaria a um script de consulta mais complexo
-- A interpretação utilizada foi de consultar somente o total de pontos obtidos no ano, e não acumulados até o ano
SELECT
    d.Forename || ' ' || d.Surname AS NomeCompletoPiloto,
    r.Year AS Ano,
    SUM(rs.Points) AS TotalPontos
FROM
    Results rs
JOIN
    Driver d ON rs.DriverId = d.DriverId
JOIN
    Races r ON rs.RaceId = r.RaceId
WHERE
    rs.Points > 0 -- Considerar apenas resultados onde pontos foram marcados (opcional, mas comum)
GROUP BY
    Ano,                    
    d.DriverId,             -- Agrupa por piloto (usar ID é mais seguro que nome)
    NomeCompletoPiloto      -- Inclui o nome no group by por ser usado no SELECT
ORDER BY
    Ano DESC,               
    TotalPontos DESC;
	
	
-- Exercício 2
SELECT year, COUNT(*) AS race_count
	FROM RACES
	GROUP BY year
	ORDER BY year DESC;

-- Exercício 3
SELECT
    Continent AS Continente,
    Type AS TipoAeroporto,
    COUNT(*) AS NumeroDeAeroportos
FROM
    Airports
GROUP BY
    Continente,  
    TipoAeroporto 
ORDER BY
    Continente ASC,  -- Ordena os continentes alfabeticamente
    NumeroDeAeroportos DESC; -- Depois ordena por tipo com mais aeroportos para com menos
	

-- Exercício 4
--podium_position como char(6) pois só assume NULL ou 'podium'
ALTER TABLE QUALIFYING
	ADD COLUMN Podium_Position CHAR(6);

UPDATE QUALIFYING
	SET Podium_Position = 'podium'
	--Apesar de position ser num e não int, between funciona
	WHERE Position BETWEEN 1 AND 3;

--Mostrado só 10 pois são muitas tuplas porém foi verificado que casos onde o piloto saiu entre os 3 o novo atributo foi setado corretamente
SELECT * 
	FROM QUALIFYING
	LIMIT 10;


-- Exercício 5
UPDATE Driver
SET
    Nationality = 'BR'
WHERE 
    Nationality = 'Brazilian';

-- Verificação da tabela após o comando do exercício
/*
SELECT DriverId, Forename, Surname, Nationality
FROM Driver
WHERE Nationality = 'Brazilian';
*/


-- Exercício 6
SELECT D.Forename || ' ' || D.Surname AS NomeCompletoPiloto, COUNT(*) AS Pole_Position_Starts
	FROM QUALIFYING Q
	--Junta DRIVERS e QUALIFYING quando IDs do piloto são iguais e se somente saiu como primeiro
	JOIN DRIVER D ON Q.driverid = D.driverid
		WHERE Q.Position = 1
	--Agrupa por nome
	GROUP BY NomeCompletoPiloto
	ORDER BY Pole_Position_Starts DESC;
	

-- Exercício 7
--Identifica os códigos e nomes dos países que sediam corridas
WITH RaceHostingCountries AS (
    SELECT DISTINCT
        C.Code,
        C.Name
    FROM
        Circuits Cir
    JOIN
        Countries C ON Cir.Country = C.Name
),
--Conta o número de cidades por código de país
CityCounts AS (
    SELECT
        Country AS CountryCode,
        COUNT(*) AS NumeroDeCidades
    FROM
        GeoCities15K
    GROUP BY
        Country
),
--Conta o número de aeroportos por código de país
AirportCounts AS (
    SELECT
        ISOCountry AS CountryCode,
        COUNT(*) AS NumeroDeAeroportos
    FROM
        Airports
    GROUP BY
        ISOCountry
)
--Junta tudo: Países que sediam corridas com suas contagens de cidades e aeroportos
SELECT
    RHC.Name AS Pais,
    CC.NumeroDeCidades AS TotalCidadesNoPais,
    AC.NumeroDeAeroportos AS TotalAeroportosNoPais
FROM
    RaceHostingCountries RHC -- Começa com os países que têm corridas
LEFT JOIN
    CityCounts CC ON RHC.Code = CC.CountryCode -- Junta a contagem de cidades
LEFT JOIN
    AirportCounts AC ON RHC.Code = AC.CountryCode -- Junta a contagem de aeroportos
ORDER BY
    RHC.Name;
	
	
-- Exercício 8
--Copia de identica COUNTRIES
CREATE TABLE COUNTRIESV2 AS
	SELECT *
	FROM COUNTRIES;

--Deleta tuplas de COUNTRIESV2
DELETE FROM COUNTRIESV2
	--Filtra as tuplas nas quais o atributo code não se encontra no conjunto seguinte 
	WHERE code NOT IN (
    	SELECT C.Code
    		FROM COUNTRIESV2 C
			--Junta COUNTRIESV2 E AIRPORTS quando códigos iso são iguais
    		JOIN AIRPORTS A ON C.Code = A.ISOCountry
			--Agrupa as tuplas pais+aeroporto por pais
    		GROUP BY C.Code
			--Restringe o conjunto a quem tem uma qtde menor que 10 tuplas por agrupamento
    		HAVING COUNT(A.ISOCountry) < 10
	);

