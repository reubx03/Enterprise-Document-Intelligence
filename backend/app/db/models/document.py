import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Document(Base):
    """
    Stores metadata about uploaded documents.
    """

    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
    )

    file_size: Mapped[int]

    status: Mapped[str] = mapped_column(
        String(50),
        default="uploaded",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )