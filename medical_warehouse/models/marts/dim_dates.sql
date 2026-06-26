{{ config(materialized='table') }}

WITH dates AS (

    SELECT DISTINCT

        DATE(message_timestamp) AS full_date

    FROM {{ ref('stg_telegram_messages') }}

    WHERE message_timestamp IS NOT NULL

)

SELECT

    TO_CHAR(full_date, 'YYYYMMDD')::INTEGER AS date_key,

    full_date,

    EXTRACT(ISODOW FROM full_date)::INTEGER AS day_of_week,

    TO_CHAR(full_date, 'Day') AS day_name,

    EXTRACT(WEEK FROM full_date)::INTEGER AS week_of_year,

    EXTRACT(MONTH FROM full_date)::INTEGER AS month,

    TO_CHAR(full_date, 'Month') AS month_name,

    EXTRACT(QUARTER FROM full_date)::INTEGER AS quarter,

    EXTRACT(YEAR FROM full_date)::INTEGER AS year,

    CASE
        WHEN EXTRACT(ISODOW FROM full_date) IN (6,7)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend

FROM dates

ORDER BY full_date