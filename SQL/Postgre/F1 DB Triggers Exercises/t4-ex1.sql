SET search_path TO "Grupo10";

--Ex1
CREATE OR REPLACE FUNCTION VerificaAeroporto()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se um valor de cidade foi fornecido na linha nova ou atualizada.
    -- Se a cidade for NULL ou vazia, a verificação não é necessária (conforme regra implícita).
    IF NEW.City IS NOT NULL AND length(NEW.City) > 0 THEN
	
        -- Verificar se a cidade fornecida (NEW.City) existe na coluna Name da tabela GeoCities15K.
        IF NOT EXISTS (SELECT 1 FROM GeoCities15K WHERE Name = NEW.City) THEN
            RAISE EXCEPTION 'Cidade nao encontrada! Operacao cancelada.';
			
        END IF;

    END IF;

    -- Se a cidade for NULL/vazia OU se a cidade foi encontrada no GeoCities15K,
    -- permitir que a operação (INSERT ou UPDATE) prossiga.
    RETURN NEW;

END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER TR_Airports
    BEFORE INSERT OR UPDATE ON Airports
    FOR EACH ROW
    EXECUTE FUNCTION VerificaAeroporto();

--Testes

--Inserção
INSERT INTO Airports (
    Id, Ident, Type, Name, LatDeg, LongDeg, ElevFt, Continent, ISOCountry,
    ISORegion, City, Scheduled_service, IATACode, GPSCode, LocalCode,
    HomeLink, WikipediaLink, Keywords
) VALUES (
    423423, 'ABC123', 'small_airport', 'Teste Aeroporto', 12.34, 56.78, 1030,
    'SA', 'BR', 'BR-SP', 'Nao Existe 123', 'no', NULL, '00TST', 'LOC123', 
    NULL, NULL, NULL
);

--Atualização
UPDATE Airports
    SET City = 'Nao Existe 123'
    WHERE Id = 6523;