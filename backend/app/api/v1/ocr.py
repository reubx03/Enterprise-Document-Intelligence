from fastapi import APIRouter, File, UploadFile

from app.schemas.ocr import OCRResponse
from app.services.ocr_service import OCRService

router = APIRouter()

ocr_service = OCRService()


@router.post(
    "/ocr",
    response_model=OCRResponse,
    summary="Extract text from a PDF document",
)
async def extract_text(
    file: UploadFile = File(...),
) -> OCRResponse:

    return await ocr_service.process_pdf(file)