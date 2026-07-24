from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.exceptions.upload_exceptions import (
    FileTooLargeError,
    InvalidFileTypeError,
)


def validate_file_type(file: UploadFile) -> None:
    """
    Validate the uploaded file extension.
    """

    extension = Path(file.filename).suffix.lower().lstrip(".")

    allowed_extensions = {
        ext.strip().lower()
        for ext in settings.allowed_file_types.split(",")
    }

    if extension not in allowed_extensions:
        raise InvalidFileTypeError(
            f"File type '{extension}' is not supported."
        )


async def validate_file_size(file: UploadFile) -> None:
    """
    Validate the uploaded file size.
    """

    content = await file.read()

    file_size = len(content)

    await file.seek(0)

    if file_size > settings.max_upload_size:
        raise FileTooLargeError(
            f"Maximum allowed file size is {settings.max_upload_size} bytes."
        )