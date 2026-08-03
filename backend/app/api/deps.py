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