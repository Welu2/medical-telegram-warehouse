WITH products AS (
    -- Get the unique list of product names from your seed file
    SELECT DISTINCT product_name
    FROM {{ ref('product_dictionary') }}
    WHERE product_name IS NOT NULL
),

messages AS (
    -- Get the actual message text (assuming column name is message_text)
    SELECT message_text
    FROM {{ ref('fct_messages') }}
    WHERE message_text IS NOT NULL
),

calculate_mentions AS (
    -- Join text using ILIKE for case-insensitive matching
    SELECT
        p.product_name,
        COUNT(m.message_text) AS mentions
    FROM products p
    LEFT JOIN messages m
        ON m.message_text ILIKE '%' || p.product_name || '%'
    GROUP BY p.product_name
)

SELECT
    product_name,
    mentions
FROM calculate_mentions
ORDER BY mentions DESC
