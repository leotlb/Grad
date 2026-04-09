-- Dashboard Piloto (1/3): Busca o nome completo do piloto e o nome de sua escuderia mais recente.
SELECT
    D.Forename || ' ' || D.Surname AS nome_piloto,
    C.Name AS nome_escuderia
FROM Driver AS D
LEFT JOIN Results RES ON D.DriverId = RES.DriverId
LEFT JOIN Races RA ON RES.RaceId = RA.RaceId
LEFT JOIN Constructors C ON RES.ConstructorId = C.ConstructorId
WHERE D.DriverId = %s
ORDER BY RA.Date DESC, RA.Round DESC
LIMIT 1;