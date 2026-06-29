from pathlib import Path
import pandas as pd
from ultralytics import YOLO

IMAGE_DIR = Path("data/raw/images")
OUTPUT_FILE = Path("data/yolo_results.csv")

model = YOLO("yolov8n.pt")


def classify_image(objects):
    """
    Categorize image based on detected objects.
    """

    has_person = "person" in objects

    product_objects = {
        "bottle",
        "cup",
        "wine glass",
        "bowl"
    }

    has_product = any(obj in product_objects for obj in objects)

    if has_person and has_product:
        return "promotional"

    if has_product:
        return "product_display"

    if has_person:
        return "lifestyle"

    return "other"


def detect():

    rows = []

    images = list(IMAGE_DIR.rglob("*"))

    for image in images:

        if image.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue

        message_id = image.stem

        result = model(str(image))[0]

        objects = []
        confidences = []

        for box in result.boxes:

            cls = int(box.cls)

            conf = float(box.conf)

            label = model.names[cls]

            objects.append(label)

            confidences.append(conf)

        rows.append({

            "message_id": message_id,

            "objects": ",".join(objects),

            "confidence_score":
                max(confidences) if confidences else 0,

            "image_category":
                classify_image(objects)

        })

    df = pd.DataFrame(rows)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(df.head())

    print(f"\nSaved {len(df)} detections to {OUTPUT_FILE}")


if __name__ == "__main__":
    detect()