class PipelineException(Exception):
    """Base exception for document processing pipeline."""


class PipelineOCRStageError(PipelineException):
    """Raised when OCR stage fails."""


class PipelineExtractionStageError(PipelineException):
    """Raised when extraction stage fails."""