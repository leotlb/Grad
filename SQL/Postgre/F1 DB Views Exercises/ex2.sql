SET search_path TO "Grupo10";
--------------------------------------------------------------------------------------
--Ex02
--Segunda view
CREATE VIEW Aeroportos_sem_cidades AS
	SELECT *
		FROM airports
		WHERE isocountry = 'BR'
		EXCEPT
			SELECT *
				FROM airports
				WHERE isocountry = 'BR' AND city IS NOT NULL;

SELECT *
	FROM Aeroportos_sem_cidades;

--Terceira view	
CREATE VIEW Cidades_brasileiras AS
	SELECT *
		FROM geocities15k
		WHERE country = 'BR' AND population >= 100000;


SELECT geonameid,name,lat,long,country,population
	FROM Cidades_brasileiras;
	LIMIT 5;
	
/*
Para realizar o cálculo da distância de Havesine é necessário a padronização dos dados de latitude e longitude.
Inicialmente, eme exercício ambas as informações geográficas de aeroportos e cidades foram como texto(varchar),
porém agora faz sentindo tratá-las como números de fato.

Para 'airports' os dados já se encontram no padrão decimal correto logo basta

ALTER TABLE airports
    ALTER COLUMN latdeg TYPE double precision USING latdeg::double precision;
ALTER TABLE airports
    ALTER COLUMN longdeg TYPE double precision USING longdeg::double precision;

Porém para a tabela "geocities15k" apesar de algumas cidades já possuirem os dados já corretamente padronizados, a maioria
possui número sem separador decimal
As latitudes e longitudes aparentam sempre ter 5 dígitos de precisão depois da casa decimal, porém variam de tamanho dependendo
da quantidade de algarismos antes da casa decimal, logo foram utilizadas expressões regulares para tratar cada um dos casos
	
UPDATE geocities15k
SET lat = 
    CASE
		--caso com formatação correta
        WHEN lat ~ '^\-?\d+(\.\d+)?$' THEN lat
	
		--caso de latitude, 1 dígito antes da vírgula, de -9 a 9
        WHEN lat ~ '^\-?\d{6}$' THEN 
            substring(lat FROM 1 FOR length(lat) - 5) || '.' || substring(lat FROM length(lat) - 4 FOR 5)
        
		--caso de latitude, 2 dígitos antes da vírgula, de -90 a 90
        WHEN lat ~ '^\-?\d{7}$' THEN 
            substring(lat FROM 1 FOR length(lat) - 5) || '.' || substring(lat FROM length(lat) - 4 FOR 5)
        
        ELSE 
            lat
    END;
UPDATE geocities15k
SET long = 
    CASE 
		--caso com formatação correta
        WHEN long ~ '^\-?\d+(\.\d+)?$' THEN long

		--caso de longitude, 1 dígito antes da vírgula, de -9 a 9
        WHEN long ~ '^\-?\d{6}$' THEN 
            substring(long FROM 1 FOR length(long) - 5) || '.' || substring(long FROM length(long) - 4 FOR 5)
        
		--caso de longitude, 2 dígitos antes da vírgula, de -99 a 99
        WHEN long ~ '^\-?\d{7}$' THEN 
            substring(long FROM 1 FOR length(long) - 5) || '.' || substring(long FROM length(long) - 4 FOR 5)
        
		--caso de longitude, 3 dígitos antes da vírgula, de -180 a 180
        WHEN long ~ '^\-?\d{8}$' THEN 
            substring(long FROM 1 FOR length(long) - 5) || '.' || substring(long FROM length(long) - 4 FOR 5)
        
        ELSE 
            long
    END;

Por fim fazendo a mudança de tipo para 'geocities15k'

ALTER TABLE geocities15k
    ALTER COLUMN lat TYPE double precision USING lat::double precision;
ALTER TABLE geocities15k
    ALTER COLUMN long TYPE double precision USING long::double precision;
	

*/

--Criando função de Haversine (não havia permissões para usar as extensões)
CREATE OR REPLACE FUNCTION haversine_distance(
    lat1 DOUBLE PRECISION, long1 DOUBLE PRECISION, 
    lat2 DOUBLE PRECISION, long2 DOUBLE PRECISION
) 
RETURNS DOUBLE PRECISION AS $$
DECLARE
    r DOUBLE PRECISION := 6371;  -- Raio médio aproximado da Terra em km
    deltaLat DOUBLE PRECISION;
    deltaLong DOUBLE PRECISION;
    a DOUBLE PRECISION;
    c DOUBLE PRECISION;
BEGIN
    -- Calculando a diferença de latitudes e longitudes
    deltaLat := radians(lat2 - lat1);
    deltaLong := radians(long2 - long1);
    
    -- Fórmula de Haversine
    a := sin(deltaLat / 2) * sin(deltaLat / 2) + 
         cos(radians(lat1)) * cos(radians(lat2)) * 
         sin(deltaLong / 2) * sin(deltaLong / 2);
    c := 2 * asin(sqrt(a));
    
    -- Retorna a distância em quilômetros
    RETURN r * c;
END;
$$ LANGUAGE plpgsql;



CREATE VIEW Aeroportos_sem_cidade_com_cidades_grandes_proximas AS
	SELECT
		a.name AS Nome_Aeroporto,
		c.name AS Nome_Cidade,
		c.population AS Populacao_Cidade,
		haversine_distance(a.latdeg, a.longdeg, c.lat, c.long) AS Distancia_km
	FROM
		Aeroportos_sem_cidades a
	JOIN 
		Cidades_brasileiras c
		ON
			haversine_distance(a.latdeg, a.longdeg, c.lat, c.long) <= 10
	ORDER BY
		a.name, c.name;
		
SELECT *
	FROM Aeroportos_sem_cidade_com_cidades_grandes_proximas;