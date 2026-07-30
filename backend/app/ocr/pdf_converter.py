from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image

from app.core.config import settings


def pdf_to_images(pdf_path: str) -> list[Image.Image]:
    """
    Convert a PDF into a list of PIL Images.
    One image is returned for each page.
    """

    pdf_file = Path(pdf_path)

    images = convert_from_path(
        pdf_file,
        dpi=settings.pdf_dpi,
        poppler_path=settings.poppler_path,
    )

    return images