-- Étape 1 : lire la donnée brute dans le schéma public de Postgres
WITH raw_data AS (
    SELECT * FROM public.raw_weather
)

-- Étape 2 : Appliquer les transformations et les règles métiers
SELECT
    id,
    city AS terminal_city,
    temperature AS temp_celsius,
    -- On convertit le vent (m/s * 3.6 = km/h) et on arrondit
    ROUND((wind_speed * 3.6)::numeric, 2) AS wind_speed_kmh,
    description AS weather_conditions,
    date_extracted,
    -- Le statut d'alerte Eurotunnel (règles métiers)
    CASE
        WHEN (wind_speed * 3.6) > 90 THEN 'ALERTE ROUGE - Risque perturbation Ferries, anticiper affluence'
        WHEN (wind_speed * 3.6) > 50 THEN 'ALERTE ORANGE - Vent fort, prudence'
        ELSE 'TRAFIC NORMAL'
    END AS eurotunnel_alert_status

FROM raw_data