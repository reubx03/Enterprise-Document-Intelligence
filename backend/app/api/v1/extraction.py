from fastapi import APIRouter

from app.services.extraction_service import ExtractionService
from app.schemas.extraction import ExtractionRequest

router = APIRouter()

service = ExtractionService()


@router.post("/extract")
def extract_document(request: ExtractionRequest):
    return service.extract(
        request.document_text
    )