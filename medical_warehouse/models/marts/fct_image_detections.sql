select
    m.message_id,
    m.channel_key,
    m.date_key,
    m.view_count,
    y.objects,
    y.confidence_score,
    y.image_category
from {{ ref('fct_messages') }} m
left join {{ ref('stg_yolo_detections') }} y
    on m.message_id = y.message_id