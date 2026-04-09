-- Insere uma nova escuderia na tabela Constructors.
-- O ID é calculado na aplicação e passado como parâmetro.
-- Uma trigger no banco de dados cria o usuário correspondente.
SET search_path TO "Grupo10";
INSERT INTO Constructors (ConstructorID, ConstructorRef, Name, Nationality, Url)
VALUES (%s, %s, %s, %s, %s);