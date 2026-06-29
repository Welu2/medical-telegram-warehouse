select
    cast(message_id as bigint) as message_id,
    objects,
    cast(confidence_score as numeric) as confidence_score,
    image_category
from analytics.raw_yolo_detections