-- Insere um novo piloto na tabela Driver.
-- O ID é calculado na aplicação e passado como parâmetro.
-- Uma trigger no banco de dados cria o usuário correspondente.
SET search_path TO "Grupo10";
INSERT INTO Driver (DriverID, DriverRef, Number, Code, Forename, Surname, Dob, Nationality, URL)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);