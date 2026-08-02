from typing import Literal

from fastapi import APIRouter, File, UploadFile

from app.services.document_processing_service import (
    DocumentProcessingService,
)

router = APIRouter()

service = DocumentProcessingService()


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
):
    return await service.process_pdf(
        file=file,
        document_type=document_type,
    )