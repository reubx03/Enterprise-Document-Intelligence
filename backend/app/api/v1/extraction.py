from fastapi import APIRouter

from app.services.extraction_service import ExtractionService

router = APIRouter()

service = ExtractionService()


@router.post("/extract")
def extract_document(document_text: str):
    return service.extract(document_text)