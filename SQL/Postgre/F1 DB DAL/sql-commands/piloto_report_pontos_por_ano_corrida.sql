-- Relatório Piloto: Lista os pontos obtidos pelo piloto em cada corrida, agrupados por ano.
-- Exibe apenas as corridas em que o piloto pontuou.
SELECT
    RA.YEAR AS "Ano",
    RA.Name AS "Nome da Corrida",
    RES.Points AS "Pontos Obtidos"
FROM Results RES
JOIN Races RA ON RES.RaceId = RA.RaceId
WHERE RES.DriverId = %s AND RES.Points > 0
ORDER BY RA.YEAR DESC, RA.Round;