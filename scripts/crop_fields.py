import cv2
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_PATH = PROJECT_ROOT / "outputs" / "cheque_aligned.jpg"
FIELDS_YAML = PROJECT_ROOT / "configs" / "fields.yaml"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "field_crops"

PADDING = 10


def load_field_config(path):
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config["fields"]


def crop_with_padding(image, box, padding=PADDING):
    x1, y1, x2, y2 = box
    h, w = image.shape[:2]
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(w, x2 + padding)
    y2 = min(h, y2 + padding)
    return image[y1:y2, x1:x2]


def main():
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        print(f"❌ عکس پیدا نشد: {IMAGE_PATH}")
        return

    fields = load_field_config(FIELDS_YAML)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for field_name, field_data in fields.items():
        box = field_data["box"]
        cropped = crop_with_padding(image, box)
        output_path = OUTPUT_DIR / f"{field_name}.jpg"
        cv2.imwrite(str(output_path), cropped)
        print(f"✅ {field_name} → {output_path}  (shape: {cropped.shape})")


if __name__ == "__main__":
    main()