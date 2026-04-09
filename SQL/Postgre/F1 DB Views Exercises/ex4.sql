SET search_path TO "Grupo10";
--------------------------------------------------------------------------------------
--Ex 4
CREATE OR REPLACE VIEW Problemas_circuitos AS
SELECT
    c.CircuitId,
    c.CircuitRef,
    c.Name,
    c.Location,
    c.Country,
    c.Lat,
    c.Lng,
    c.Alt,
    c.URL
FROM
    Circuits c
EXCEPT
SELECT
    c.CircuitId,
    c.CircuitRef,
    c.Name,
    c.Location,
    c.Country,
    c.Lat,
    c.Lng,
    c.Alt,
    c.URL
FROM
    Circuits c
INNER JOIN
    Countries co ON c.Country = co.Name;	-- Condição de junção: Circuits.Country = Countries.Name

-- Para verificar o conteúdo da visão criada:
-- SELECT * FROM Problemas_circuitos;