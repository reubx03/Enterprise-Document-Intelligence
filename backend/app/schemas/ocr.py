from pydantic import BaseModel
from typing import List


class OCRPage(BaseModel):
    page_number: int
    extracted_text: str
    average_confidence: float


class OCRResponse(BaseModel):
    filename: str
    page_count: int
    pages: List[OCRPage]
    processing_time: float
    status: str