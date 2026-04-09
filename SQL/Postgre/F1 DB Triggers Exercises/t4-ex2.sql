SET search_path TO "Grupo10";

--Ex2

--Script inicial
/*

CREATE TABLE Results_Status (
    StatusID INTEGER PRIMARY KEY,
    Contagem INTEGER,
    FOREIGN KEY (StatusID) REFERENCES Status(StatusID)
);

INSERT INTO Results_Status
SELECT S.StatusId , COUNT (*)
FROM Status S JOIN Results R ON R.StatusID = S.StatusID
GROUP BY S.StatusId , S.Status;

*/

--Itens a, b e c

CREATE OR REPLACE FUNCTION AtualizaContagem()
RETURNS TRIGGER AS $$
DECLARE
    v_nova_contagem INTEGER;
    v_nova_contagem_antiga INTEGER; -- Para o caso de UPDATE
    v_nova_contagem_atual INTEGER;  -- Para o caso de UPDATE
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE Results_Status
        SET Contagem = Contagem + 1
        WHERE StatusID = NEW.StatusID
        RETURNING Contagem INTO v_nova_contagem; -- Pega a nova contagem

        RAISE NOTICE 'StatusID: %, Contagem: %', NEW.StatusID, v_nova_contagem;

    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE Results_Status
        SET Contagem = Contagem - 1
        WHERE StatusID = OLD.StatusID
        RETURNING Contagem INTO v_nova_contagem; -- Pega a nova contagem

        RAISE NOTICE 'StatusID: %, Contagem: %', OLD.StatusID, v_nova_contagem;

    ELSIF (TG_OP = 'UPDATE') THEN
        -- Verifica se a coluna StatusID foi realmente alterada
        IF OLD.StatusID IS DISTINCT FROM NEW.StatusID THEN
            -- Diminui a contagem do StatusID antigo
            UPDATE Results_Status
            SET Contagem = Contagem - 1
            WHERE StatusID = OLD.StatusID
            RETURNING Contagem INTO v_nova_contagem_antiga; -- Pega a nova contagem do status antigo

            RAISE NOTICE 'StatusId Anterior: %, Contagem: %', OLD.StatusID, v_nova_contagem_antiga;

            -- Aumenta a contagem do StatusID novo
            UPDATE Results_Status
            SET Contagem = Contagem + 1
            WHERE StatusID = NEW.StatusID
            RETURNING Contagem INTO v_nova_contagem_atual; -- Pega a nova contagem do status atual

            RAISE NOTICE 'StatusId Atual: %, Contagem: %', NEW.StatusID, v_nova_contagem_atual;
        END IF;
    END IF;

    RETURN NULL; -- Trigger after não retorna nada

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TR_ResultsStatus
    AFTER INSERT OR DELETE OR UPDATE ON Results 
    FOR EACH ROW
    EXECUTE FUNCTION AtualizaContagem();

--Item d

CREATE OR REPLACE FUNCTION VerificaStatus()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o StatusID que será inserido ou atualizado é negativo
    IF NEW.StatusID IS NOT NULL AND NEW.StatusID < 0 THEN
        -- Se for negativo, levanta uma exceção e cancela a operação
        RAISE EXCEPTION 'StatusID Negativo! Operacao cancelada.';
    END IF;

    -- Se o StatusID não for negativo (ou for NULL), permite que a operação continue
    RETURN NEW;

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TR_Results
    BEFORE INSERT OR UPDATE ON Results
    FOR EACH ROW
    EXECUTE FUNCTION VerificaStatus();

--Testes a, b e c

--Inserção
INSERT INTO Results (
    ResultId, RaceId, DriverId, ConstructorId, Number, Grid, Position, PositionText, PositionOrder, Points,
	Laps, Time, Milliseconds, FastestLap, Rank, FastestLapTime, FastestLapSpeed, StatusId
) VALUES (
    99999, 101, 25, 7, 44, 2, 1, '1', 1, 25, 58, '1:35:27.325', 5727325,
    42, 1, '00:10:20.627', '215', 1
);

INSERT INTO Results (
    ResultId, RaceId, DriverId, ConstructorId, Number, Grid, Position, PositionText, PositionOrder, Points,
	Laps, Time, Milliseconds, FastestLap, Rank, FastestLapTime, FastestLapSpeed, StatusId
) VALUES (
    99998, 1011, 25, 7, 44, 2, 1, '1', 1, 25, 58, '1:35:27.325', 5727325,
    42, 1, '00:10:20.627', '215', 1
);

--Atualização
UPDATE Results
SET StatusId = 2
WHERE ResultId = 99999 OR ResultId = 99998;

--Remoção
DELETE FROM Results
WHERE ResultId = 99999 OR ResultId = 99998;

--Testes d

--Inserção
INSERT INTO Results (
    ResultId, RaceId, DriverId, ConstructorId, Number, Grid, Position, PositionText, PositionOrder, Points,
	Laps, Time, Milliseconds, FastestLap, Rank, FastestLapTime, FastestLapSpeed, StatusId
) VALUES (
    99999, 101, 25, 7, 44, 2, 1, '1', 1, 25, 58, '1:35:27.325', 5727325,
    42, 1, '00:10:20.627', '215', -2
);

--Atualização
INSERT INTO Results (
    ResultId, RaceId, DriverId, ConstructorId, Number, Grid, Position, PositionText, PositionOrder, Points,
	Laps, Time, Milliseconds, FastestLap, Rank, FastestLapTime, FastestLapSpeed, StatusId
) VALUES (
    99999, 101, 25, 7, 44, 2, 1, '1', 1, 25, 58, '1:35:27.325', 5727325,
    42, 1, '00:10:20.627', '215', 2
);

UPDATE Results
SET StatusId = -2
WHERE ResultId = 99999;