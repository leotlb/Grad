SET search_path TO "Grupo10";

--Ex1
CREATE OR REPLACE FUNCTION Nome_Nacionalidade(construtor_nome TEXT)
RETURNS TEXT AS $$
DECLARE
    construtor_nacionalidade TEXT;
BEGIN
	RAISE NOTICE 'Procurando construtor: %', construtor_nome;
    SELECT nationality INTO construtor_nacionalidade
    	FROM constructors
    	WHERE name = construtor_nome;

	IF construtor_nacionalidade IS NULL THEN
        RAISE NOTICE 'Construtor "%" nao esta na base de dados', construtor_nome;
        RETURN 'Nao encontrado';
    END IF;

    RETURN construtor_nacionalidade;
END;
$$ LANGUAGE plpgsql;

SELECT Nome_Nacionalidade('Ferrari') AS Nacionalidade
UNION ALL
SELECT Nome_Nacionalidade('Williams') AS Nacionalidade
UNION ALL
SELECT Nome_Nacionalidade('Renault') AS Nacionalidade
UNION ALL
SELECT Nome_Nacionalidade('Toro Rosso') AS Nacionalidade
UNION ALL
SELECT Nome_Nacionalidade('Lada') AS Nacionalidade;

--------------------------------------------------------------------------------------

--Ex2
CREATE OR REPLACE FUNCTION Pilotos_Nacionalidade(piloto_nacionalidade TEXT)
RETURNS VOID AS
$$
DECLARE
    r RECORD;
    counter INT := 1;
BEGIN
    FOR r IN
        SELECT forename, surname
        	FROM driver
        	WHERE nationality = piloto_nacionalidade
        	ORDER BY forename, surname
    LOOP
        RAISE NOTICE '% Name: % %', counter, r.forename, r.surname;
        counter := counter + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM Pilotos_Nacionalidade('German');

--------------------------------------------------------------------------------------

--Ex3
CREATE OR REPLACE FUNCTION Cidade_Chamada(cidade_nome TEXT)
RETURNS VOID AS $$
DECLARE
    cidade_counter INT := 1;
	cidade RECORD;
BEGIN
	RAISE NOTICE 'Procurando cidades chamadas: %', cidade_nome;
    FOR cidade IN 
        SELECT name, population, country
        FROM geocities15k
        WHERE name = cidade_nome
    LOOP
        RAISE NOTICE 'Contagem: %| Nome: %, Populacao: %, Pais: %',
            cidade_counter, cidade.name, cidade.population, cidade.country;
        cidade_counter := cidade_counter + 1;
    END LOOP;

	IF cidade_counter = 1 THEN
        RAISE NOTICE 'Nenhuma cidade encontrada com o nome: %', cidade_nome;
    END IF;
END;
$$ LANGUAGE plpgsql;

SELECT Cidade_Chamada('York');
SELECT Cidade_Chamada('São Carlos');

--------------------------------------------------------------------------------------

--Ex4
CREATE OR REPLACE FUNCTION Numero_vitorias(
    piloto_nome TEXT,
    piloto_sobrenome TEXT,
    ano_vitorias NUMERIC(4) DEFAULT NULL
)
RETURNS INT AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)
	        FROM driver d
	        JOIN results res ON d.driverID = res.driverID
	        JOIN races rac ON res.raceID = rac.raceID
	        	WHERE d.forename = piloto_nome
	          		AND d.surname = piloto_sobrenome
	          		AND res.position = 1
	          		AND (ano_vitorias IS NULL OR rac.year = ano_vitorias)
    );
END;
$$ LANGUAGE plpgsql;

SELECT Numero_vitorias('Lewis', 'Hamilton', 2019);

--------------------------------------------------------------------------------------

--Ex5
CREATE OR REPLACE FUNCTION Pais_Continente()
RETURNS TABLE(Nome VARCHAR, Continente CHAR(2)) AS
$$
DECLARE
    pais_record RECORD;
    pais_cursor CURSOR FOR
        SELECT c.name, c.continent
        	FROM countries c
        	WHERE LENGTH(name) <= 15;
BEGIN
	--Abre cursor
    OPEN pais_cursor;
    LOOP
		--Pega a tupla que cursor aponta e coloca no RECORD
        FETCH pais_cursor INTO pais_record;
		--Quando cursor iterou sobre todo o SELECT quebra o loop
        EXIT WHEN NOT FOUND;
		--Retorna os atributos do RECORD em uma tupla da tabela resultado
        RETURN QUERY SELECT pais_record.name, pais_record.continent;
    END LOOP;
	--Fecha cursor
    CLOSE pais_cursor;
    RETURN;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM Pais_Continente();

--------------------------------------------------------------------------------------

--Ex6
SET search_path TO "Grupo10";

CREATE OR REPLACE FUNCTION Valida_Volta(
    nome_autodromo TEXT,
    pais_autodromo TEXT,
    ano INT,
    nome_piloto TEXT,
    sobrenome_piloto TEXT,
    numero_volta INT
)
RETURNS TABLE (id_piloto INT, id_corrida INT, status INT) AS
$$
DECLARE
    temp_driverid INT;
    temp_raceid INT;
    temp_circuitid INT;
    ultima_volta INT;
BEGIN
	--Verificação se o piloto existe
    SELECT driverid INTO temp_driverid
    	FROM driver
    	WHERE forename = nome_piloto AND surname = sobrenome_piloto
    	LIMIT 1;
    IF NOT FOUND THEN
        RETURN QUERY SELECT NULL::INT, NULL::INT, 3;
		RETURN;
    END IF;

	--Verificação se o autodromo existe
    SELECT circuitid INTO temp_circuitid
    	FROM circuits
    	WHERE name = nome_autodromo AND country = pais_autodromo
    	LIMIT 1;
    IF NOT FOUND THEN
        RETURN QUERY SELECT NULL::INT, NULL::INT, 4;
		RETURN;
    END IF;

	--Verificação se o corrida ocorrendo nesse autodromo nesse ano existe
    SELECT raceid INTO temp_raceid
    	FROM races rac
    	WHERE rac.circuitid = temp_circuitid AND rac.year = ano
    	LIMIT 1;
    IF NOT FOUND THEN
        RETURN QUERY SELECT NULL::INT, NULL::INT, 5;
		RETURN;
    END IF;

	-- Verifica se existe um registro do piloto completando a volta em questão
	IF EXISTS (
		--Seleciona a ocorrencia da volta a ser inserida
        SELECT 1
        	FROM laptimes
        	WHERE raceid = temp_raceid AND driverid = temp_driverid AND lap = numero_volta
    ) THEN
		--A volta a ser cadastrada só pode sobrescrever um registro já existente
        RETURN QUERY SELECT temp_driverid, temp_raceid, 1;
		RETURN;
	END IF;
	
	--Seleciona maior volta e coloca em ultima_volta
    SELECT MAX(lap) INTO ultima_volta
    	FROM laptimes
   		WHERE raceid = temp_raceid AND driverid = temp_driverid;
	--Se select anterior retorna nulo (não há voltas)
    IF NOT FOUND THEN
		--Cadastrando primeira volta
        IF numero_volta = 1 THEN
            RETURN QUERY SELECT temp_driverid, temp_raceid, 2;
			RETURN;
		--Cadastrando volta posterior sem o piloto ter volta alguma registrada
        ELSE
            RETURN QUERY SELECT temp_driverid, temp_raceid, 6;
			RETURN;
        END IF;
    END IF;
	--Cadastrando próxima volta sem o piloto ter volta anterior registrada
    IF ultima_volta + 1 != numero_volta THEN
        RETURN QUERY SELECT temp_driverid, temp_raceid, 6;
		RETURN;
    END IF;

	--A volta a ser cadastrada preenche todos requisitos e pode ser inserida
    RETURN QUERY SELECT temp_driverid, temp_raceid, 0;
	RETURN;
END;
$$ LANGUAGE plpgsql;


SELECT * 
	FROM Valida_Volta('Bahrain International Circuit', 'Bahrain', 2023, 'Kevin', 'Magnussen', 56);

