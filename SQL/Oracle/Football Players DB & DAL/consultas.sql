--Consulta 1 (Média Complexidade): Listar o nome das pessoas matriculadas em alguma modalidade,
--o nome da modalidade e a unidade, exibindo apenas as modalidades
--relacionadas a São Carlos.
SELECT P.NOME AS Pessoa, M.MODALIDADE AS Modalidade, M.UNIDADE AS Unidade
FROM MATRICULA M
INNER JOIN PESSOA P ON M.PESSOA = P.CPF
WHERE M.UNIDADE = 'São Carlos';

--Consulta 2 (Média Complexidade): Contar quantas modalidades diferentes existem em cada unidade.
SELECT UNIDADE, COUNT(DISTINCT MODALIDADE) AS TotalModalidades
FROM MODALIDADE
GROUP BY UNIDADE;

--Consulta 3 (Alta Complexidade): Listar os nomes das
--pessoas que estão matriculadas em modalidades que têm um menor associado.
SELECT DISTINCT P.NOME AS Pessoa
FROM PESSOA P
WHERE P.CPF IN (
    SELECT M.PESSOA
    FROM MATRICULA M
    WHERE M.MODALIDADE IN (
        SELECT NOME
        FROM MODALIDADE
        WHERE MENOR IS NOT NULL
    )
);

--Consulta 4 (Alta Complexidade): Exibir os nomes das modalidades e os responsáveis, incluindo
--apenas modalidades que têm pelo menos um treino particular agendado.
SELECT MOD.NOME AS Modalidade, PESS.NOME AS Responsavel
FROM MODALIDADE MOD
INNER JOIN RESPONSAVEL R ON MOD.RESPONSAVEL = R.CPF
INNER JOIN PESSOA PESS ON R.CPF = PESS.CPF
WHERE EXISTS (
    SELECT 1
    FROM TREINO_PARTICULAR T
    WHERE T.PERSONAL = R.CPF
);

--Consulta 5 (Média Complexidade): Listar todas as pessoas cadastradas,
--incluindo as que não possuem matrícula em nenhuma modalidade, exibindo
--também o nome da modalidade, se houver.
SELECT P.NOME AS Pessoa, M.MODALIDADE AS Modalidade
FROM PESSOA P
LEFT JOIN MATRICULA M ON P.CPF = M.PESSOA;

--Consulta 6 (Alta Complexidade): Exibir o número de treinos particulares realizados por cada
--personal e o local onde mais treinos foram realizados.
SELECT T.PERSONAL, COUNT(*) AS TotalTreinos, MAX(T.LOCAL) AS LocalMaisUtilizado
FROM TREINO_PARTICULAR T
GROUP BY T.PERSONAL
HAVING COUNT(*) > 1; -- Considerar apenas personals com mais de 1 treino

--Consulta 7 (Alta Complexidade): Listar os nomes das pessoas matriculadas em modalidades que
--possuem treinadores pessoais associados.
SELECT P.NOME AS Pessoa
FROM PESSOA P
WHERE EXISTS (
    SELECT 1
    FROM MATRICULA M
    INNER JOIN PERSONAL PR ON M.MODALIDADE = PR.MODALIDADE
    WHERE M.PESSOA = P.CPF
);

--Consulta 8 (Alta Complexidade): Listar todas as modalidades registradas, seus responsáveis
--e os menores associados, incluindo modalidades que não possuem menores associados.
SELECT MOD.NOME AS Modalidade, MOD.UNIDADE AS Unidade, PESS.NOME AS Responsavel, MENOR.NOME AS Menor
FROM MODALIDADE MOD
LEFT JOIN RESPONSAVEL R ON MOD.RESPONSAVEL = R.CPF
LEFT JOIN PESSOA PESS ON R.CPF = PESS.CPF
LEFT JOIN PESSOA MENOR ON MOD.MENOR = MENOR.CPF
ORDER BY MOD.UNIDADE, MOD.NOME;

--Consulta 9 (Média Complexidade): Listar todos os CPFs de pessoas que são responsáveis
--ou que já fizeram algum treino particular.
SELECT R.CPF
FROM RESPONSAVEL R
UNION
SELECT T.PESSOA
FROM TREINO_PARTICULAR T;

--Consulta 10 (Alta Complexidade. Utiliza divisão relacional): Encontrar pessoas
--matriculadas em todas as modalidades disponíveis.
SELECT P.NOME AS Pessoa
FROM PESSOA P
WHERE NOT EXISTS (
    SELECT MOD.NOME
    FROM MODALIDADE MOD
    WHERE NOT EXISTS (
        SELECT M.PESSOA
        FROM MATRICULA M
        WHERE M.PESSOA = P.CPF AND M.MODALIDADE = MOD.NOME
    )
);