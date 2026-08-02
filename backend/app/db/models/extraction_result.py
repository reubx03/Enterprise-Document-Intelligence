import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class ExtractionResult(Base):
    """
    Stores AI extraction results for a processed document.
    """

    __tablename__ = "extraction_results"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id"),
    )

    document_type: Mapped[str]

    fields: Mapped[dict] = mapped_column(
        JSONB,
    )

    overall_confidence: Mapped[float] = mapped_column(
        Float,
    )

    requires_review: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )