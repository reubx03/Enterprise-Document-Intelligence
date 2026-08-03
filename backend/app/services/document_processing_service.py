from fastapi import UploadFile

from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.extraction_repository import (
    ExtractionResultRepository,
)
from app.db.repositories.ocr_repository import OCRResultRepository
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

    Persists a Document, OCRResult, and ExtractionResult row via the
    injected repositories at each stage boundary, including on failure.

    OCRService and ExtractionService remain database-agnostic; this
    service is the only place that knows persistence exists.
    """

    def __init__(
        self,
        document_repo: DocumentRepository,
        ocr_repo: OCRResultRepository,
        extraction_repo: ExtractionResultRepository,
    ):
        self.ocr_service = OCRService()
        self.extraction_service = ExtractionService()
        self.document_repo = document_repo
        self.ocr_repo = ocr_repo
        self.extraction_repo = extraction_repo

    async def process_pdf(
        self,
        file: UploadFile,
        document_type: str = "auto",
    ):
        # -----------------------------
        # Create the document record
        # -----------------------------
        print("\n===== Creating Document =====")

        document = self.document_repo.create(
            original_filename=file.filename,
            content_type=file.content_type,
            file_size=0,
        )

        print(f"Document created: {document.id}")

        # -----------------------------
        # Stage 1 - OCR
        # -----------------------------
        try:
            print("\n===== Starting OCR =====")

            ocr_result = await self.ocr_service.process_pdf(file)

            print("OCR completed successfully.")

        except OCRException as e:
            self.document_repo.update_status(document.id, "failed")
            raise PipelineOCRStageError(
                f"OCR stage failed: {e}"
            ) from e

        # Combine all page text
        document_text = "\n\n".join(
            page.extracted_text
            for page in ocr_result.pages
        )

        if ocr_result.pages:
            ocr_average_confidence = sum(
                page.average_confidence
                for page in ocr_result.pages
            ) / len(ocr_result.pages)
        else:
            ocr_average_confidence = 0.0

        print("Saving OCR result...")

        self.ocr_repo.create(
            document_id=document.id,
            page_count=ocr_result.page_count,
            full_text=document_text,
            average_confidence=ocr_average_confidence,
            processing_time=ocr_result.processing_time,
        )

        print("OCR result saved.")

        self.document_repo.update_status(
            document.id,
            "ocr_complete",
        )

        print("Document status updated -> ocr_complete")

        # -----------------------------
        # Stage 2 - Extraction
        # -----------------------------
        try:
            print("\n===== Starting Extraction =====")

            extraction_result = self.extraction_service.extract(
                document_text=document_text,
                document_type=document_type,
            )

            print("Extraction completed.")

        except ExtractionException as e:
            self.document_repo.update_status(document.id, "failed")
            raise PipelineExtractionStageError(
                f"Extraction stage failed: {e}"
            ) from e

        print("Saving extraction result...")

        self.extraction_repo.create(
            document_id=document.id,
            document_type=extraction_result["document_type"],
            fields=extraction_result["fields"],
            overall_confidence=extraction_result["overall_confidence"],
            requires_review=extraction_result["requires_review"],
        )

        print("Extraction result saved.")

        print("Updating document status -> extraction_complete")

        self.document_repo.update_status(
            document.id,
            "extraction_complete",
        )

        print("Document status updated successfully.")

        extraction_result["document_id"] = str(
            document.id
        )

        print("\n===== Pipeline Finished Successfully =====\n")

        return extraction_result