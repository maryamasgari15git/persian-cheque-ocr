import os
from pathlib import Path

turbojpeg_dir = r"C:\libjpeg-turbo64\bin"
if os.path.exists(turbojpeg_dir):
    os.add_dll_directory(turbojpeg_dir)

import cv2
import numpy as np
from docaligner import DocAligner

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_PATH = PROJECT_ROOT / "data" / "samples" / "check3.jpg"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "cheque_aligned.jpg"

TEMPLATE_WIDTH = 1200
TEMPLATE_HEIGHT = 600


def warp_to_template(image, corners, width=TEMPLATE_WIDTH, height=TEMPLATE_HEIGHT):
    src = np.array(corners, dtype="float32")
    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")
    matrix = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(image, matrix, (width, height))


def main():
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        print(f"❌ عکس پیدا نشد: {IMAGE_PATH}")
        return

    print(f"✅ عکس خونده شد. ابعاد: {image.shape}")

    model = DocAligner()
    corners = model(image)
    print("گوشه‌های تشخیص داده شده:")
    print(corners)

    warped = warp_to_template(image, corners)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUTPUT_PATH), warped)
    print(f"✅ عکس صاف‌شده ذخیره شد: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()