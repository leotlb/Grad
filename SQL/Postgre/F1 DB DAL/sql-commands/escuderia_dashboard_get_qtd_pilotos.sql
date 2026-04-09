-- Dashboard Escuderia (3/4): Conta o número de pilotos distintos que já correram pela escuderia logada.
SELECT COUNT(DISTINCT DriverId) AS qtd_pilotos FROM Results WHERE ConstructorId = %s;