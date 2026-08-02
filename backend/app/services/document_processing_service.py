from fastapi import UploadFile

from app.services.ocr_service import OCRService
from app.services.extraction_service import ExtractionService


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
        # Stage 1 - OCR
        ocr_result = await self.ocr_service.process_pdf(file)

        # Combine all page text
        document_text = "\n\n".join(
            page.extracted_text
            for page in ocr_result.pages
        )

        # Stage 2 - Extraction
        extraction_result = self.extraction_service.extract(
            document_text=document_text,
            document_type=document_type,
        )

        return extraction_result