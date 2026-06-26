-- This test ensures that no message is dated in the future
-- It should return 0 rows to pass

SELECT
    message_id,
    message_timestamp
FROM {{ ref('stg_telegram_messages') }}
WHERE message_timestamp > NOW()