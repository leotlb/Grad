-- Valida as credenciais do usuário (login e senha) na tabela USERS.
-- Retorna UserId, Tipo e IdOriginal se as credenciais forem válidas.
SET search_path TO "Grupo10";
SELECT UserId, Tipo, IdOriginal FROM USERS WHERE Login = %s AND Password = %s;