class OCRException(Exception):
    """Base exception for OCR-related errors."""
    pass


class InvalidPDFError(OCRException):
    """Raised when an invalid PDF is provided."""
    pass


class PDFConversionError(OCRException):
    """Raised when PDF to image conversion fails."""
    pass


class OCRProcessingError(OCRException):
    """Raised when OCR processing fails."""
    pass