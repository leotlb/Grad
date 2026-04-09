-- Insere um registro de atividade do usuário (login/logout) na tabela Users_Log.
-- Utiliza funções do PostgreSQL para data e hora atuais.
INSERT INTO Users_Log (UserId, data_evento, hora_evento, tipo_evento)
VALUES (%s, CURRENT_DATE, CURRENT_TIME, %s);