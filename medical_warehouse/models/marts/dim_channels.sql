{{ config(materialized='table') }}

WITH channels AS (

    SELECT
        channel_name,
        channel_username,
        MIN(message_timestamp) AS first_post_date,
        MAX(message_timestamp) AS last_post_date,
        COUNT(message_id) AS total_posts,
        AVG(view_count) AS avg_views

    FROM {{ ref('stg_telegram_messages') }}

    GROUP BY
        channel_name,
        channel_username

)

SELECT

    ROW_NUMBER() OVER (ORDER BY channel_name) AS channel_key,

    channel_name,

    channel_username,

    CASE

        WHEN LOWER(channel_name) LIKE '%pharma%' THEN 'Pharmaceutical'

        WHEN LOWER(channel_name) LIKE '%cosmetic%' THEN 'Cosmetics'

        WHEN LOWER(channel_name) LIKE '%beauty%' THEN 'Cosmetics'

        WHEN LOWER(channel_name) LIKE '%med%' THEN 'Medical'

        ELSE 'Other'

    END AS channel_type,

    first_post_date,

    last_post_date,

    total_posts,

    ROUND(avg_views,2) AS avg_views

FROM channels
