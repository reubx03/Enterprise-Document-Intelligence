class ExtractionException(Exception):
    """Base exception for extraction errors."""


class LLMProviderError(ExtractionException):
    """Raised when the configured LLM provider request fails."""


class MalformedExtractionResponseError(ExtractionException):
    """Raised when the LLM returns invalid or unexpected output."""


class UnsupportedDocumentTypeError(ExtractionException):
    """Raised when the document type cannot be processed."""