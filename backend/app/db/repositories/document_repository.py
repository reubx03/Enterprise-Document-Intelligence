from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document import Document


class DocumentRepository:
    """
    Handles all database operations related to Documents.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        original_filename: str,
        content_type: str,
        file_size: int,
    ) -> Document:

        document = Document(
            original_filename=original_filename,
            content_type=content_type,
            file_size=file_size,
            status="uploaded",
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def get_by_id(
        self,
        document_id: UUID,
    ) -> Document | None:

        return (
            self.db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 50,
    ):

        return (
            self.db.query(Document)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_status(
        self,
        document_id: UUID,
        status: str,
    ):

        document = self.get_by_id(document_id)

        if document is None:
            return None

        document.status = status

        self.db.commit()
        self.db.refresh(document)

        return document