from fastapi import APIRouter

from app.services.extraction_service import ExtractionService
from app.schemas.extraction import ExtractionRequest

router = APIRouter()

service = ExtractionService()


@router.post("/extract")
def extract_document(request: ExtractionRequest):
    return service.extract(
        document_text=request.document_text,
        document_type=request.document_type,
    )