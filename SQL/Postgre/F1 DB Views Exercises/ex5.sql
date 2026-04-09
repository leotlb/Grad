SET search_path TO "Grupo10";
--------------------------------------------------------------------------------------
--Ex 5
CREATE OR REPLACE VIEW Correcao_circuitos AS
SELECT
    Name,       -- Vem diretamente da tabela Circuits, via Problemas_circuitos
    Location,   -- Vem diretamente da tabela Circuits, via Problemas_circuitos
    Country     -- Este é o atributo problemático da tabela Circuits
FROM
    Problemas_circuitos;
/*

-- Para verificar o conteúdo da visão criada e para resolução do exercício:
SELECT * FROM Correcao_circuitos;
SELECT * FROM Circuits EXCEPT (SELECT * FROM Problemas_circuitos);
-- Ao comparar as seleções, nota-se valores inconsistentes na tabela,
-- como USA (United States), Korea, UK (United Kingdom)

-- Correções:
-- Comando de Atualização para 'USA' -> 'United States'
UPDATE Circuits
SET Country = 'United States'
WHERE Country = 'USA';
-- Comando de Atualização para 'UK' -> 'United Kingdom'
UPDATE Circuits
SET Country = 'United Kingdom'
WHERE Country = 'UK';
-- Comando de Atualização para 'Korea' -> 'South Korea'
UPDATE Circuits
SET Country = 'South Korea'
WHERE Country = 'Korea';
-- Comando de Atualização para 'UAE' -> 'United Arab Emirates'
UPDATE Circuits
SET Country = 'United Arab Emirates'
WHERE Country = 'UAE';

-- Verificação final
SELECT COUNT(*) AS ProblemasRestantes FROM Problemas_circuitos;

*/