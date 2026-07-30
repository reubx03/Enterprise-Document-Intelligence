import cv2
import numpy as np
from PIL import Image


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Improve image quality before OCR.
    """

    # Convert PIL Image to NumPy array
    img = np.array(image)

    # Convert RGB to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Apply Otsu Thresholding
    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Convert back to PIL Image
    return Image.fromarray(thresh)