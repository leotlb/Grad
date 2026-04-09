SET search_path TO "Grupo10";
-------------------------------------------------------------------------------------------------------
--Ex1

-- Alterações para adequar ao retorno de Mede_tempo
ALTER TABLE Driver
	ALTER COLUMN forename
	SET DATA TYPE TEXT;

ALTER TABLE Driver
	ALTER COLUMN surname
	SET DATA TYPE TEXT;

ALTER TABLE Driver
	ALTER COLUMN nationality
	SET DATA TYPE TEXT;

-- Função corrigida váriavel Diff e melhorado o NOTICE
CREATE OR REPLACE FUNCTION Mede_Tempo(Q TEXT)
	RETURNS TABLE (Name TEXT , Nationality TEXT) AS $$
	DECLARE
		TIni TIME; TFim TIME;
		i DOUBLE PRECISION;
		Diff BIGINT;
	BEGIN
		-- Registra o tempo inicial
		TIni := CLOCK_TIMESTAMP();
		FOR i IN 0..100 LOOP
			EXECUTE Q;
		END LOOP;
		-- Registra o tempo final
		TFim := CLOCK_TIMESTAMP();
		-- Calcula a diferenca em milisegundos
		-- TFim - Tini resulta em um INTERVAL
		-- EXTRACT(EPOCH ... resulta em um DOUBLE PRECISION com o número de segundos
		-- Multiplica por 1000 pra expor em milisegundos
		-- ROUND arrendonda e transforma DOUBLE PRECISION em um BIGINT
		Diff := ROUND(EXTRACT(EPOCH FROM TFim - TIni) * 1000);
		RAISE NOTICE 'Tempo Inicial: %  Tempo Final: % Duracao da Execucao(ms): %', TFim , TIni , Diff;
		-- Retorna o resultado da consulta recebida
	RETURN QUERY EXECUTE Q;
END;
$$ LANGUAGE plpgsql;


/*
Consulta a ser feita

SELECT 
    forename || ' ' || surname AS nome_completo, nationality
	FROM driver
	WHERE forename || ' ' || surname = 'Ayrton Senna';
*/

-- Consulta sem índice
SELECT * FROM Mede_Tempo(
    $$SELECT 
        forename || ' ' || surname AS Name,
        nationality
    FROM driver
    WHERE forename || ' ' || surname = 'Ayrton Senna'$$
);

CREATE INDEX IdxNome_completo
	ON driver ((forename || ' ' || surname)) 
	INCLUDE (nationality);

-- Consulta com índice
SELECT * FROM Mede_Tempo(
    $$SELECT 
        forename || ' ' || surname AS Name,
        nationality
    FROM driver
    WHERE forename || ' ' || surname = 'Ayrton Senna'$$
);

-------------------------------------------------------------------------------------------------------
Ex2

-- Correcao do tipo na tabela das cidades
ALTER TABLE geocities15k
	ALTER COLUMN name
	SET DATA TYPE TEXT;

-- Remove a função antiga para atualizar seu retorno
DROP FUNCTION Mede_Tempo(TEXT);

-- Nova funcão com retorno ajustado
CREATE OR REPLACE FUNCTION Mede_Tempo(Q TEXT)
	RETURNS TABLE (Name TEXT , Latitude DOUBLE PRECISION, Longitude DOUBLE PRECISION, Population INTEGER) AS $$
	DECLARE
		TIni TIME; TFim TIME;
		i DOUBLE PRECISION;
		Diff BIGINT;
	BEGIN
		-- Registra o tempo inicial
		TIni := CLOCK_TIMESTAMP();
		FOR i IN 0..100 LOOP
			EXECUTE Q;
		END LOOP;
		-- Registra o tempo final
		TFim := CLOCK_TIMESTAMP();
		-- Calcula a diferenca em milisegundos
		-- TFim - Tini resulta em um INTERVAL
		-- EXTRACT(EPOCH ... resulta em um DOUBLE PRECISION com o número de segundos
		-- Multiplica por 1000 pra expor em milisegundos
		-- ROUND arrendonda e transforma DOUBLE PRECISION em um BIGINT
		Diff := ROUND(EXTRACT(EPOCH FROM TFim - TIni) * 1000);
		RAISE NOTICE 'Tempo Inicial: % | Tempo Final: % | Duracao da Execucao(ms): %', TFim , TIni , Diff;
		-- Retorna o resultado da consulta recebida
	RETURN QUERY EXECUTE Q;
END;
$$ LANGUAGE plpgsql;

/*
Consulta desejada:
SELECT name, lat, long, population
	FROM geocities15k
	WHERE country = 'BR' 
	AND name LIKE 'Ribeirão%'
	ORDER BY population DESC;

*/

-- Consulta sem índice
SELECT * FROM Mede_Tempo(
    $$SELECT name, lat, long, population
		FROM geocities15k
		WHERE country = 'BR' 
		AND name LIKE 'Ribeirão%'
		ORDER BY population DESC;$$
);

CREATE INDEX IdxCidadesBrasileiras
	ON geocities15k (name)
	INCLUDE (lat,long,population)
	WHERE country = 'BR';

-- Consulta com índice
SELECT * FROM Mede_Tempo(
    $$SELECT name, lat, long, population
		FROM geocities15k
		WHERE country = 'BR' 
		AND name LIKE 'Ribeirão%'
		ORDER BY population DESC;$$
);