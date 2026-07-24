from pathlib import Path
from uuid import uuid4


def generate_unique_filename(original_filename: str) -> tuple[str, str]:
    """
    Generate a unique filename while preserving the extension.

    Returns:
        document_id,
        generated_filename
    """

    extension = Path(original_filename).suffix.lower()

    document_id = str(uuid4())

    generated_filename = f"{document_id}{extension}"

    return document_id, generated_filename