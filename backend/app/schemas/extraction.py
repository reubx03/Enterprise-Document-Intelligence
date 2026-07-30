from typing import Literal

from pydantic import BaseModel, Field


class DocumentField(BaseModel):
    field_name: str = Field(
        ...,
        description="Name of the extracted field."
    )

    value: str | None = Field(
        default=None,
        description="Extracted value."
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score."
    )

    source_text: str | None = Field(
        default=None,
        description="Original supporting text."
    )


class ExtractionResponse(BaseModel):
    document_type: Literal[
        "invoice",
        "resume",
        "contract",
        "purchase_order",
        "receipt",
        "bank_statement",
        "unknown",
    ]

    fields: list[DocumentField]

    overall_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    processing_time: float

    requires_review: bool

    status: Literal[
        "success",
        "failed",
    ]

    document_id: str | None = None