from typing import Literal

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.deps import get_document_processing_service
from app.services.document_processing_service import (
    DocumentProcessingService,
)

router = APIRouter()


@router.post("/documents/process")
async def process_document(
    file: UploadFile = File(...),
    document_type: Literal[
        "invoice",
        "resume",
        "contract",
        "purchase_order",
        "receipt",
        "bank_statement",
        "auto",
    ] = "auto",
    service: DocumentProcessingService = Depends(
        get_document_processing_service
    ),
):
    return await service.process_pdf(
        file=file,
        document_type=document_type,
    )