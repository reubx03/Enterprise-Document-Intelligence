from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.extraction_result import ExtractionResult


class ExtractionResultRepository:
    """
    Handles database operations related to extraction results.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        document_id: UUID,
        document_type: str,
        fields: dict,
        overall_confidence: float,
        requires_review: bool,
    ) -> ExtractionResult:

        result = ExtractionResult(
            document_id=document_id,
            document_type=document_type,
            fields=fields,
            overall_confidence=overall_confidence,
            requires_review=requires_review,
        )

        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result

    def get_by_document_id(
        self,
        document_id: UUID,
    ) -> ExtractionResult | None:

        return (
            self.db.query(ExtractionResult)
            .filter(
                ExtractionResult.document_id == document_id
            )
            .first()
        )