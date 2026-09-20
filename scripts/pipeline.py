import os
from pathlib import Path

turbojpeg_dir = r"C:\libjpeg-turbo64\bin"
if os.path.exists(turbojpeg_dir):
    os.add_dll_directory(turbojpeg_dir)

import cv2
import numpy as np
import yaml
from docaligner import DocAligner

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIELDS_YAML = PROJECT_ROOT / "configs" / "fields.yaml"

TEMPLATE_WIDTH = 1200
TEMPLATE_HEIGHT = 600
PADDING = 10

_model = None  # مدل رو فقط یه‌بار لود می‌کنیم، نه هر بار که یه عکس میاد


def get_model():
    global _model
    if _model is None:
        _model = DocAligner()
    return _model


def align_image(image, width=TEMPLATE_WIDTH, height=TEMPLATE_HEIGHT):
    model = get_model()
    corners = model(image)

    src = np.array(corners, dtype="float32")
    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(image, matrix, (width, height))
    return warped


def load_field_config():
    with open(FIELDS_YAML, "r", encoding="utf-8") as f:
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


def process_cheque(image):
    """
    ورودی: تصویر خام چک (numpy array)
    خروجی: (عکس صاف‌شده, دیکشنری {اسم فیلد: عکس crop شده})
    """
    aligned = align_image(image)

    fields = load_field_config()
    crops = {}
    for field_name, field_data in fields.items():
        box = field_data["box"]
        crops[field_name] = crop_with_padding(aligned, box)

    return aligned, crops