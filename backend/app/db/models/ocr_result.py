import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class OCRResult(Base):
    """
    Stores OCR output for a processed document.
    """

    __tablename__ = "ocr_results"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id"),
    )

    page_count: Mapped[int] = mapped_column(
        Integer,
    )

    full_text: Mapped[str] = mapped_column(
        Text,
    )

    average_confidence: Mapped[float] = mapped_column(
        Float,
    )

    processing_time: Mapped[float] = mapped_column(
        Float,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )