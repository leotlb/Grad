-- Dashboard Escuderia (2/4): Conta o número de vitórias (Position=1) da escuderia logada.
SELECT COUNT(*) AS vitorias FROM Results WHERE ConstructorId = %s AND Position = 1;