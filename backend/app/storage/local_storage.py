from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.exceptions.upload_exceptions import FileStorageError


class LocalStorage:
    """
    Handles saving uploaded files to local storage.
    """

    async def save_file(
        self,
        file: UploadFile,
        filename: str,
    ) -> Path:

        upload_dir = Path(settings.upload_directory)

        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / filename

        try:
            content = await file.read()

            with open(file_path, "wb") as f:
                f.write(content)

            await file.seek(0)

            return file_path

        except Exception as e:
            raise FileStorageError(
                f"Failed to save file: {e}"
            )