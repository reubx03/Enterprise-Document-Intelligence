from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.exceptions.upload_exceptions import FileStorageError


class LocalStorage:
    """
    Handles saving and deleting files in local storage.
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

            # Reset file pointer so it can be read again if needed
            await file.seek(0)

            return file_path

        except Exception as e:
            raise FileStorageError(
                f"Failed to save file: {e}"
            )

    def delete_file(
        self,
        file_path: Path,
    ) -> None:
        """
        Deletes a file from local storage.
        """

        try:
            if file_path.exists():
                file_path.unlink()

        except Exception as e:
            raise FileStorageError(
                f"Failed to delete file: {e}"
            )