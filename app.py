import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse

from utils import perform_ocr

app = FastAPI()

@app.post("/ocr/")
async def ocr_receipt(file: UploadFile):
    # Check if the uploaded file is an image
    if file.content_type.startswith("image"):
        image_bytes = await file.read()
        img_array = np.frombuffer(image_bytes, np.uint8)

        ocr_text = perform_ocr(img_array)
        return JSONResponse(content={"result": ocr_text}, status_code=200)
    else:
        return {"error": "Uploaded file is not an image"}

