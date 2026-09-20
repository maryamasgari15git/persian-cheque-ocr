import cv2
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_PATH = PROJECT_ROOT / "outputs" / "cheque_aligned.jpg"
OUTPUT_YAML = PROJECT_ROOT / "configs" / "fields.yaml"


def main():
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        print(f"❌ عکس پیدا نشد: {IMAGE_PATH}")
        return

    print("راهنما:")
    print("- با ماوس دور هر فیلد یه مستطیل بکشید")
    print("- بعد از کشیدن هر مستطیل، کلید ENTER یا SPACE بزنید تا تأیید بشه")
    print("- برای فیلد بعدی دوباره بکشید و ENTER بزنید")
    print("- وقتی همه‌ی فیلدها رو کشیدید، کلید ESC بزنید تا تموم بشه")
    print()

    boxes = cv2.selectROIs(
        "Select Fields (ENTER=confirm box, ESC=finish)",
        image,
        fromCenter=False,
        showCrosshair=True
    )
    cv2.destroyAllWindows()

    if len(boxes) == 0:
        print("هیچ فیلدی انتخاب نشد.")
        return

    print(f"\n{len(boxes)} تا فیلد انتخاب شد. حالا برای هرکدوم اسم بدید:\n")

    fields = {}
    for i, (x, y, w, h) in enumerate(boxes):
        box = [int(x), int(y), int(x + w), int(y + h)]
        print(f"فیلد شماره {i + 1}: مختصات = {box}")
        name = input("  اسم این فیلد: ").strip()
        if name:
            fields[name] = {"box": box}

    OUTPUT_YAML.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_YAML, "w", encoding="utf-8") as f:
        yaml.dump({"fields": fields}, f, allow_unicode=True)

    print(f"\n✅ ذخیره شد تو {OUTPUT_YAML}")


if __name__ == "__main__":
    main()