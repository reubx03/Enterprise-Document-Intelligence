from datetime import datetime

from fastapi import UploadFile

from app.schemas.upload import UploadResponse
from app.storage.local_storage import LocalStorage
from app.utils.file_validation import (
    validate_file_size,
    validate_file_type,
)
from app.utils.filename_generator import (
    generate_unique_filename,
)


class UploadService:

    def __init__(self):
        self.storage = LocalStorage()

    async def upload_file(
        self,
        file: UploadFile,
    ) -> UploadResponse:

        # Validate file
        validate_file_type(file)
        await validate_file_size(file)

        # Generate unique filename
        document_id, generated_filename = generate_unique_filename(
            file.filename
        )

        # Save file
        await self.storage.save_file(
            file=file,
            filename=generated_filename,
        )

        # Build response
        return UploadResponse(
            document_id=document_id,
            filename=generated_filename,
            original_filename=file.filename,
            content_type=file.content_type,
            file_size=file.size,
            upload_time=datetime.utcnow(),
            status="uploaded",
        )