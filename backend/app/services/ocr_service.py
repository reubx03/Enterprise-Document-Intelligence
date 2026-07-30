import time

from fastapi import UploadFile

from app.exceptions.ocr_exceptions import (
    OCRProcessingError,
)
from app.ocr.image_preprocessor import preprocess_image
from app.ocr.pdf_converter import pdf_to_images
from app.ocr.tesseract_engine import extract_text
from app.schemas.ocr import OCRPage, OCRResponse
from app.storage.local_storage import LocalStorage
from app.utils.filename_generator import generate_unique_filename


class OCRService:

    def __init__(self) -> None:
        self.storage = LocalStorage()

    async def process_pdf(
        self,
        file: UploadFile,
    ) -> OCRResponse:

        document_id, filename = generate_unique_filename(
            file.filename
        )

        file_path = await self.storage.save_file(
            file=file,
            filename=filename,
        )

        start = time.time()

        try:
            images = pdf_to_images(str(file_path))

            pages = []

            for index, image in enumerate(
                images,
                start=1,
            ):
                processed = preprocess_image(image)

                text, confidence = extract_text(
                    processed
                )

                pages.append(
                    OCRPage(
                        page_number=index,
                        extracted_text=text,
                        average_confidence=confidence,
                    )
                )

            return OCRResponse(
                filename=file.filename,
                page_count=len(pages),
                pages=pages,
                processing_time=round(
                    time.time() - start,
                    2,
                ),
                status="success",
            )

        except Exception as e:
            raise OCRProcessingError(
                f"OCR processing failed: {e}"
            )

        finally:
            self.storage.delete_file(file_path)