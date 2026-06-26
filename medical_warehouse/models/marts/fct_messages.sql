{{ config(materialized='table') }}

WITH messages AS (

    SELECT
        message_id,
        channel_name,
        message_timestamp,
        message_text,
        message_length,
        view_count,
        forward_count,
        has_image

    FROM {{ ref('stg_telegram_messages') }}

),

channels AS (

    SELECT
        channel_key,
        channel_name

    FROM {{ ref('dim_channels') }}

),

dates AS (

    SELECT
        date_key,
        full_date

    FROM {{ ref('dim_dates') }}

)

SELECT

    m.message_id,

    c.channel_key,

    d.date_key,

    m.message_text,

    m.message_length,

    m.view_count,

    m.forward_count,

    m.has_image

FROM messages m

LEFT JOIN channels c
    ON m.channel_name = c.channel_name

LEFT JOIN dates d
    ON DATE(m.message_timestamp) = d.full_date