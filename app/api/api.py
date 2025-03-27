import shutil
import os
from typing import Any

from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.models.predict import PredictRequest, PredictResponse
from app.services.pdf_parser import PDFParserService

api_router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@api_router.post("/processing/")
async def upload_pdf(file: UploadFile = File(...)):
    # Проверяем MIME-тип
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parser = PDFParserService(file_path)
    content = parser.extract_text()

    return JSONResponse(content={"filename": file.filename, "message": "File was parsed", "content": content})

@api_router.post("/predict", response_model=PredictResponse)
async def predict(request: Request, payload: PredictRequest) -> Any:
    """
    ML Prediction API
    """
    input_text = payload.input_text
    model = request.app.state.model

    predict_value = model.predict(input_text)
    return PredictResponse(result=predict_value)
