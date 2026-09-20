import sys
from pathlib import Path
import cv2
import numpy as np
import base64

sys.path.append(str(Path(__file__).resolve().parent / "scripts"))
from pipeline import process_cheque

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def image_to_base64(image):
    _, buffer = cv2.imencode(".jpg", image)
    return base64.b64encode(buffer).decode("utf-8")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if image is None:
        return templates.TemplateResponse(request, "index.html", {
            "error": "نتونستم فایل رو به‌عنوان عکس بخونم."
        })

    aligned, crops = process_cheque(image)

    aligned_b64 = image_to_base64(aligned)
    crops_b64 = {name: image_to_base64(img) for name, img in crops.items()}

    return templates.TemplateResponse(request, "index.html", {
        "aligned_image": aligned_b64,
        "crops": crops_b64
    })