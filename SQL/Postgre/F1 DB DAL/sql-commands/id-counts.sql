---

-- ==============================================================================================
-- == Tabela para contagem de IDs de Drivers e Constructors
-- ==============================================================================================
DROP TABLE IF EXISTS ID_Counts CASCADE;
CREATE TABLE ID_Counts (
    -- Coluna para armazenar a contagem de DriverIds
    DriverCount INTEGER DEFAULT 0,
    -- Coluna para armazenar a contagem de ConstructorIds
    ConstructorCount INTEGER DEFAULT 0
);

-- Insere as contagens iniciais na tabela ID_Counts
-- Isso garante que a tabela comece com os valores corretos dos dados já existentes
INSERT INTO ID_Counts (DriverCount, ConstructorCount)
SELECT
    (SELECT COUNT(*) FROM Driver),
    (SELECT COUNT(*) FROM Constructors);

-- ==============================================================================================
-- == Funções de Gatilho para atualizar ID_Counts
-- = ============================================================================================

-- Função de gatilho para atualizar a contagem de Drivers
-- Esta função será executada sempre que um novo Driver for inserido.
CREATE OR REPLACE FUNCTION update_driver_count_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza a coluna DriverCount na tabela ID_Counts, incrementando em 1
    UPDATE ID_Counts
    SET DriverCount = DriverCount + 1;
    RETURN NEW; -- Retorna a nova linha inserida (necessário para gatilhos AFTER INSERT)
END;
$$ LANGUAGE plpgsql;

-- Função de gatilho para atualizar a contagem de Constructors
-- Esta função será executada sempre que um novo Constructor for inserido.
CREATE OR REPLACE FUNCTION update_constructor_count_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza a coluna ConstructorCount na tabela ID_Counts, incrementando em 1
    UPDATE ID_Counts
    SET ConstructorCount = ConstructorCount + 1;
    RETURN NEW; -- Retorna a nova linha inserida (necessário para gatilhos AFTER INSERT)
END;
$$ LANGUAGE plpgsql;

-- ==============================================================================================
-- == Definição dos Gatilhos (Triggers)
-- ==============================================================================================

-- Gatilho para a tabela Driver
-- Será ativado APÓS uma inserção em Driver, para cada linha (FOR EACH ROW)
-- e executará a função update_driver_count_trigger_func.
CREATE TRIGGER after_driver_insert
AFTER INSERT ON Driver
FOR EACH ROW
EXECUTE FUNCTION update_driver_count_trigger_func();

-- Gatilho para a tabela Constructors
-- Será ativado APÓS uma inserção em Constructors, para cada linha (FOR EACH ROW)
-- e executará a função update_constructor_count_trigger_func.
CREATE TRIGGER after_constructor_insert
AFTER INSERT ON Constructors
FOR EACH ROW
EXECUTE FUNCTION update_constructor_count_trigger_func();
