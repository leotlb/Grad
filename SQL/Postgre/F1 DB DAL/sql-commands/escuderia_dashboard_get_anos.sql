-- Dashboard Escuderia (4/4): Busca o primeiro e o último ano em que a escuderia logada participou de corridas.
SELECT MIN(RA.YEAR) AS primeiro_ano, MAX(RA.YEAR) AS ultimo_ano
FROM Results AS RES JOIN Races AS RA ON RES.RaceId = RA.RaceId
WHERE RES.ConstructorId = %s;