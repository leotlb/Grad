SET search_path TO "Grupo10";

-- Remove objetos antigos para garantir que a criação seja limpa
DROP TRIGGER IF EXISTS constructors_sync_users_trigger ON constructors;
DROP TRIGGER IF EXISTS driver_sync_users_trigger ON driver;
DROP FUNCTION IF EXISTS trg_sync_constructor_to_users();
DROP FUNCTION IF EXISTS trg_sync_driver_to_users();
DROP TABLE IF EXISTS Users_Log;
DROP TABLE IF EXISTS USERS;

--================================================================================
--== Tabela de Usuários                                                         ==
--================================================================================
CREATE TABLE USERS (
  UserId SERIAL PRIMARY KEY,
  Login TEXT UNIQUE NOT NULL,
  Password TEXT NOT NULL,
  Tipo VARCHAR(20) NOT NULL CHECK (Tipo IN ('Administrador', 'Escuderia', 'Piloto')),
  IdOriginal INTEGER -- FK para driverId ou constructorId, ou NULL para admin
);

COMMENT ON TABLE USERS IS 'Armazena as credenciais e tipos de usuários para acesso à aplicação.';
COMMENT ON COLUMN USERS.IdOriginal IS 'ID da tabela original (Constructors ou Driver) para o usuário correspondente.';


--================================================================================
--== Tabela de Log de Acesso                                                    ==
--================================================================================
CREATE TABLE Users_Log (
  LogId SERIAL PRIMARY KEY,
  UserId INTEGER REFERENCES USERS(UserId) ON DELETE SET NULL,
  data_evento DATE NOT NULL DEFAULT CURRENT_DATE,
  hora_evento TIME NOT NULL DEFAULT CURRENT_TIME,
  tipo_evento VARCHAR(10) NOT NULL CHECK (tipo_evento IN ('login', 'logout'))
);

COMMENT ON TABLE Users_Log IS 'Audita todos os eventos de login e logout no sistema.';


--================================================================================
--== Trigger para sincronizar CONSTRUCTORS -> USERS                             ==
--================================================================================
CREATE OR REPLACE FUNCTION trg_sync_constructor_to_users()
RETURNS TRIGGER AS $$
DECLARE
  v_login TEXT;
  v_password TEXT;
BEGIN
  -- Define o padrão de login e senha baseado no ConstructorRef
  v_login := NEW.ConstructorRef || '_c';
  v_password := NEW.ConstructorRef;

  -- Se a operação for uma INSERÇÃO de nova escuderia
  IF TG_OP = 'INSERT' THEN
    -- Verifica se o login já existe para evitar duplicidade
    IF EXISTS (SELECT 1 FROM USERS WHERE Login = v_login) THEN
      RAISE EXCEPTION 'Login "%" já existe. A inserção na tabela CONSTRUCTORS foi cancelada.', v_login;
    END IF;
    
    -- Insere o novo usuário na tabela USERS
    INSERT INTO USERS (Login, Password, Tipo, IdOriginal)
    VALUES (v_login, v_password, 'Escuderia', NEW.ConstructorId);

  -- Se a operação for uma ATUALIZAÇÃO de uma escuderia existente
  ELSIF TG_OP = 'UPDATE' THEN
    -- Apenas executa se o ConstructorRef (que afeta o login) for alterado
    IF OLD.ConstructorRef IS DISTINCT FROM NEW.ConstructorRef THEN
      -- Verifica se o NOVO login já está em uso por OUTRO usuário
      IF EXISTS (SELECT 1 FROM USERS WHERE Login = v_login AND IdOriginal != NEW.ConstructorId) THEN
        RAISE EXCEPTION 'O novo login "%" já pertence a outro usuário. A atualização foi cancelada.', v_login;
      END IF;

      -- Atualiza o login e senha do usuário correspondente
      UPDATE USERS SET Login = v_login, Password = v_password
      WHERE Tipo = 'Escuderia' AND IdOriginal = NEW.ConstructorId;
    END IF;
  END IF;

  -- Permite que a operação (INSERT/UPDATE) na tabela CONSTRUCTORS continue
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Cria o gatilho que aciona a função acima antes de inserir ou atualizar CONSTRUCTORS
CREATE TRIGGER constructors_sync_users_trigger
BEFORE INSERT OR UPDATE ON Constructors
FOR EACH ROW EXECUTE FUNCTION trg_sync_constructor_to_users();

COMMENT ON TRIGGER constructors_sync_users_trigger ON Constructors IS 'Mantém a tabela USERS sincronizada com as inserções e atualizações de escuderias.';


--================================================================================
--== Trigger para sincronizar DRIVER -> USERS                                   ==
--================================================================================
CREATE OR REPLACE FUNCTION trg_sync_driver_to_users()
RETURNS TRIGGER AS $$
DECLARE
  v_login TEXT;
  v_password TEXT;
BEGIN
  -- Define o padrão de login e senha baseado no DriverRef
  v_login := NEW.DriverRef || '_d';
  v_password := NEW.DriverRef;

  -- Se a operação for uma INSERÇÃO de novo piloto
  IF TG_OP = 'INSERT' THEN
    -- Verifica se o login já existe para evitar duplicidade
    IF EXISTS (SELECT 1 FROM USERS WHERE Login = v_login) THEN
      RAISE EXCEPTION 'Login "%" já existe. A inserção na tabela DRIVER foi cancelada.', v_login;
    END IF;
    
    -- Insere o novo usuário na tabela USERS
    INSERT INTO USERS (Login, Password, Tipo, IdOriginal)
    VALUES (v_login, v_password, 'Piloto', NEW.DriverId);

  -- Se a operação for uma ATUALIZAÇÃO de um piloto existente
  ELSIF TG_OP = 'UPDATE' THEN
    -- Apenas executa se o DriverRef (que afeta o login) for alterado
    IF OLD.DriverRef IS DISTINCT FROM NEW.DriverRef THEN
      -- Verifica se o NOVO login já está em uso por OUTRO usuário
      IF EXISTS (SELECT 1 FROM USERS WHERE Login = v_login AND IdOriginal != NEW.DriverId) THEN
        RAISE EXCEPTION 'O novo login "%" já pertence a outro usuário. A atualização foi cancelada.', v_login;
      END IF;
      
      -- Atualiza o login e senha do usuário correspondente
      UPDATE USERS SET Login = v_login, Password = v_password
      WHERE Tipo = 'Piloto' AND IdOriginal = NEW.DriverId;
    END IF;
  END IF;

  -- Permite que a operação (INSERT/UPDATE) na tabela DRIVER continue
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Cria o gatilho que aciona a função acima antes de inserir ou atualizar DRIVER
CREATE TRIGGER driver_sync_users_trigger
BEFORE INSERT OR UPDATE ON Driver
FOR EACH ROW EXECUTE FUNCTION trg_sync_driver_to_users();

COMMENT ON TRIGGER driver_sync_users_trigger ON Driver IS 'Mantém a tabela USERS sincronizada com as inserções e atualizações de pilotos.';


--================================================================================
--== População Inicial da Tabela de Usuários                                    ==
--================================================================================
-- 1. Inserir o usuário administrador padrão
INSERT INTO USERS (Login, Password, Tipo)
VALUES ('admin', 'admin', 'Administrador')
ON CONFLICT (Login) DO NOTHING;

-- 2. Popular a tabela USERS com dados existentes da tabela Constructors
INSERT INTO USERS (Login, Password, Tipo, IdOriginal)
SELECT ConstructorRef || '_c', ConstructorRef, 'Escuderia', ConstructorId
FROM Constructors
ON CONFLICT (Login) DO NOTHING; -- Ignora escuderias que já tenham um usuário correspondente

-- 3. Popular a tabela USERS com dados existentes da tabela Driver
INSERT INTO USERS (Login, Password, Tipo, IdOriginal)
SELECT DriverRef || '_d', DriverRef, 'Piloto', DriverId
FROM Driver
ON CONFLICT (Login) DO NOTHING; -- Ignora pilotos que já tenham um usuário correspondente

-- Verifica a criação
SELECT Tipo, COUNT(*) FROM USERS GROUP BY Tipo;
