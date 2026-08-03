from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.ocr_result import OCRResult


class OCRResultRepository:
    """
    Handles database operations related to OCR results.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        document_id: UUID,
        page_count: int,
        full_text: str,
        average_confidence: float,
        processing_time: float,
    ) -> OCRResult:

        result = OCRResult(
            document_id=document_id,
            page_count=page_count,
            full_text=full_text,
            average_confidence=average_confidence,
            processing_time=processing_time,
        )

        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result

    def get_by_document_id(
        self,
        document_id: UUID,
    ) -> OCRResult | None:

        return (
            self.db.query(OCRResult)
            .filter(OCRResult.document_id == document_id)
            .first()
        )