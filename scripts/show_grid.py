import cv2
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "outputs" / "cheque_aligned.jpg"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "cheque_grid.jpg"


def draw_grid(image, step=50):
    grid_img = image.copy()
    h, w = image.shape[:2]

    for x in range(0, w, step):
        cv2.line(grid_img, (x, 0), (x, h), (0, 255, 0), 1)
        cv2.putText(grid_img, str(x), (x + 2, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    for y in range(0, h, step):
        cv2.line(grid_img, (0, y), (w, y), (0, 255, 0), 1)
        cv2.putText(grid_img, str(y), (2, y + 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    return grid_img


if __name__ == "__main__":
    image = cv2.imread(str(INPUT_PATH))
    if image is None:
        print(f"❌ عکس پیدا نشد: {INPUT_PATH}")
    else:
        grid_img = draw_grid(image)
        cv2.imwrite(str(OUTPUT_PATH), grid_img)
        print(f"✅ ذخیره شد: {OUTPUT_PATH}")