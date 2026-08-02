from fastapi import UploadFile

from app.exceptions.extraction_exceptions import (
    ExtractionException,
)
from app.exceptions.ocr_exceptions import (
    OCRException,
)
from app.exceptions.pipeline_exceptions import (
    PipelineExtractionStageError,
    PipelineOCRStageError,
)
from app.services.extraction_service import ExtractionService
from app.services.ocr_service import OCRService


class DocumentProcessingService:
    """
    Coordinates the complete document processing pipeline.

    Upload File
        ↓
    OCR
        ↓
    Extraction
    """

    def __init__(self):
        self.ocr_service = OCRService()
        self.extraction_service = ExtractionService()

    async def process_pdf(
        self,
        file: UploadFile,
        document_type: str = "auto",
    ):
        # -----------------------------
        # Stage 1 - OCR
        # -----------------------------
        try:
            ocr_result = await self.ocr_service.process_pdf(file)

        except OCRException as e:
            raise PipelineOCRStageError(
                f"OCR stage failed: {e}"
            ) from e

        # Combine all page text
        document_text = "\n\n".join(
            page.extracted_text
            for page in ocr_result.pages
        )

        # -----------------------------
        # Stage 2 - Extraction
        # -----------------------------
        try:
            extraction_result = self.extraction_service.extract(
                document_text=document_text,
                document_type=document_type,
            )

        except ExtractionException as e:
            raise PipelineExtractionStageError(
                f"Extraction stage failed: {e}"
            ) from e

        return extraction_result