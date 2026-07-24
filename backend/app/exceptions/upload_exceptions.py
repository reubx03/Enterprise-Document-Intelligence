class UploadException(Exception):
    """Base exception for upload-related errors."""
    pass


class InvalidFileTypeError(UploadException):
    """Raised when an unsupported file type is uploaded."""
    pass


class FileTooLargeError(UploadException):
    """Raised when uploaded file exceeds the maximum allowed size."""
    pass


class FileStorageError(UploadException):
    """Raised when file storage fails."""
    pass