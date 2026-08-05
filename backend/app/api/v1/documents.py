from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.deps import (
    get_document_processing_service,
    get_document_query_service,
)
from app.services.document_processing_service import (
    DocumentProcessingService,
)
from app.services.document_query_service import (
    DocumentQueryService,
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
        get_document_processing_service,
    ),
):
    return await service.process_pdf(
        file=file,
        document_type=document_type,
    )


@router.get("/documents")
def list_documents(
    skip: int = 0,
    limit: int = 50,
    service: DocumentQueryService = Depends(
        get_document_query_service,
    ),
):
    return service.list_documents(
        skip=skip,
        limit=limit,
    )


@router.get("/documents/{document_id}")
def get_document(
    document_id: UUID,
    service: DocumentQueryService = Depends(
        get_document_query_service,
    ),
):
    result = service.get_document(document_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return result