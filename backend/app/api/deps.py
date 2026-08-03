from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.repositories.document_repository import (
    DocumentRepository,
)
from app.db.repositories.extraction_repository import (
    ExtractionResultRepository,
)
from app.db.repositories.ocr_repository import (
    OCRResultRepository,
)
from app.db.session import get_db
from app.services.document_processing_service import (
    DocumentProcessingService,
)
from app.services.document_query_service import (
    DocumentQueryService,
)


def get_document_repository(
    db: Session = Depends(get_db),
) -> DocumentRepository:
    return DocumentRepository(db)


def get_ocr_repository(
    db: Session = Depends(get_db),
) -> OCRResultRepository:
    return OCRResultRepository(db)


def get_extraction_repository(
    db: Session = Depends(get_db),
) -> ExtractionResultRepository:
    return ExtractionResultRepository(db)


def get_document_processing_service(
    document_repo: DocumentRepository = Depends(
        get_document_repository
    ),
    ocr_repo: OCRResultRepository = Depends(
        get_ocr_repository
    ),
    extraction_repo: ExtractionResultRepository = Depends(
        get_extraction_repository
    ),
) -> DocumentProcessingService:
    return DocumentProcessingService(
        document_repo=document_repo,
        ocr_repo=ocr_repo,
        extraction_repo=extraction_repo,
    )


def get_document_query_service(
    document_repo: DocumentRepository = Depends(
        get_document_repository
    ),
    ocr_repo: OCRResultRepository = Depends(
        get_ocr_repository
    ),
    extraction_repo: ExtractionResultRepository = Depends(
        get_extraction_repository
    ),
) -> DocumentQueryService:
    return DocumentQueryService(
        document_repo=document_repo,
        ocr_repo=ocr_repo,
        extraction_repo=extraction_repo,
    )