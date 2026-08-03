from uuid import UUID

from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.extraction_repository import (
    ExtractionResultRepository,
)
from app.db.repositories.ocr_repository import (
    OCRResultRepository,
)


class DocumentQueryService:
    """
    Handles document retrieval operations.
    """

    def __init__(
        self,
        document_repo: DocumentRepository,
        ocr_repo: OCRResultRepository,
        extraction_repo: ExtractionResultRepository,
    ):
        self.document_repo = document_repo
        self.ocr_repo = ocr_repo
        self.extraction_repo = extraction_repo

    def get_document(
        self,
        document_id: UUID,
    ):
        document = self.document_repo.get_by_id(document_id)

        if document is None:
            return None

        ocr = self.ocr_repo.get_by_document_id(document_id)
        extraction = self.extraction_repo.get_by_document_id(
            document_id
        )

        return {
            "document": document,
            "ocr": ocr,
            "extraction": extraction,
        }

    def list_documents(
        self,
        skip: int = 0,
        limit: int = 50,
    ):
        return self.document_repo.list_all(
            skip=skip,
            limit=limit,
        )