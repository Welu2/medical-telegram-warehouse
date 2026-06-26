{{ config(materialized='view') }}

WITH source AS (

    SELECT *
    FROM raw.telegram_messages

),

cleaned AS (

    SELECT

        -- Primary Key
        CAST(id AS BIGINT) AS message_id,

        -- Channel Information
        TRIM(channel_name) AS channel_name,
        TRIM(channel_username) AS channel_username,

        -- Message
        TRIM(message) AS message_text,

        -- Timestamp
        CAST(message_date AS TIMESTAMP) AS message_timestamp,

        -- Metrics
        COALESCE(CAST(views AS INTEGER), 0) AS view_count,
        COALESCE(CAST(forwards AS INTEGER), 0) AS forward_count,

        -- Image
        COALESCE(has_image, FALSE) AS has_image,
        image_path,

        -- Derived Fields
        LENGTH(COALESCE(message, '')) AS message_length,

        -- Keep raw JSON for debugging if needed
        raw_json

    FROM source

)

SELECT *

FROM cleaned

WHERE
    message_text IS NOT NULL
    AND message_text <> ''