-- Dashboard Piloto (2/3): Busca o primeiro e o último ano em que o piloto logado participou de corridas.
SELECT MIN(RA.YEAR) AS primeiro_ano, MAX(RA.YEAR) AS ultimo_ano
FROM Results AS RES JOIN Races AS RA ON RES.RaceId = RA.RaceId
WHERE RES.DriverId = %s;