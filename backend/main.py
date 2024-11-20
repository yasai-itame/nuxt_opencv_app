from fastapi import FastAPI, Form, File, UploadFile, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import base64
import numpy as np
import cv2

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.post("/result-opencv")
async def upload_image(type: str = Form(...), file: UploadFile = File(...)):
    content_type = file.content_type
    contents = await file.read()

    print(type)

    # NumPy配列に変換
    np_array = np.frombuffer(contents, np.uint8)
    
    # OpenCVで画像データとして読み込む
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    if img is None:
        return JSONResponse(content={"error": "Could not decode image"}, status_code=400)
    
    if type == 'gray':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if type == 'mosaic':
        small = cv2.resize(img, dsize=None, fx=0.1 , fy=0.1, interpolation=cv2.INTER_NEAREST)
        img = cv2.resize(small, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    if type == 'edge':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.Canny(gray, 100, 200)

    if type == 'rotation':
        img = cv2.flip(img, 1)
    
    _, buffer = cv2.imencode(".png", img)

    encode_image = base64.b64encode(buffer).decode("utf-8")

    file.file.close()

    return JSONResponse(content={"encode_image": encode_image, "content_type": content_type, "format": "png"})
