import pytesseract
from PIL import Image

from app.core.config import settings


# Configure Tesseract executable
pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


def extract_text(image: Image.Image) -> tuple[str, float]:
    """
    Extract text and average confidence from an image.
    """

    data = pytesseract.image_to_data(
        image,
        lang=settings.ocr_language,
        output_type=pytesseract.Output.DICT
    )

    words = []
    confidences = []

    for text, conf in zip(data["text"], data["conf"]):
        if text.strip():
            words.append(text)

            try:
                conf_value = float(conf)
                if conf_value >= 0:
                    confidences.append(conf_value)
            except ValueError:
                continue

    extracted_text = " ".join(words)

    average_confidence = (
        sum(confidences) / len(confidences)
        if confidences
        else 0.0
    )

    return extracted_text, average_confidence