-- Relatório Admin: Encontra aeroportos próximos (até 100km) de uma cidade específica no Brasil.
SET search_path TO "Grupo10";

-- A consulta externa seleciona e filtra os resultados da consulta interna.
-- Isso permite calcular a distância uma única vez e usá-la tanto no SELECT quanto no WHERE.
SELECT
  "Nome da Cidade",
  "Código IATA",
  "Nome do Aeroporto",
  "Cidade do Aeroporto",
  ROUND("Distância (Km)"::numeric, 2) AS "Distância (Km)", -- Arredonda o resultado final
  "Tipo do Aeroporto"
FROM (
    -- A consulta interna calcula a distância para cada aeroporto.
    SELECT
      ci.nome_cidade_base AS "Nome da Cidade",
      ap.IATACode AS "Código IATA",
      ap.Name AS "Nome do Aeroporto",
      ap.City AS "Cidade do Aeroporto",
      ap.Type AS "Tipo do Aeroporto",
      
      -- Início da Fórmula de Haversine
      -- 6371 é o raio médio da Terra em quilômetros.
      -- As latitudes e longitudes são convertidas de graus para radianos.
      (
        6371 * 2 * ASIN(SQRT(
            POWER(SIN((RADIANS(ap.LatDeg) - ci.lat_rad) / 2), 2) +
            COS(ci.lat_rad) * COS(RADIANS(ap.LatDeg)) *
            POWER(SIN((RADIANS(ap.LongDeg) - ci.lon_rad) / 2), 2)
        ))
      ) AS "Distância (Km)"
      -- Fim da Fórmula de Haversine

    FROM
      Airports ap,
      -- A CTE 'cidade_info' obtém as coordenadas da cidade base já em radianos.
      (
        SELECT
          Name AS nome_cidade_base,
          RADIANS(Lat) as lat_rad,
          RADIANS(Long) as lon_rad
        FROM GeoCities15K
        WHERE Name ILIKE %s
        LIMIT 1 -- Pega a cidade mais populosa com esse nome
      ) as ci
    WHERE
      -- Filtra para aeroportos relevantes no Brasil antes de calcular a distância.
      ap.ISOCountry = 'BR' AND ap.Type IN ('medium_airport', 'large_airport')
) AS airports_with_distance
-- Filtra o resultado final para aeroportos dentro de um raio de 100 km.
WHERE "Distância (Km)" <= 100
ORDER BY "Distância (Km)";