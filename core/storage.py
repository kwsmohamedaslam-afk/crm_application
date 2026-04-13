import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

from core.config import settings
from utils.logger import logger


ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}

ALLOWED_DOC_TYPES = {"application/pdf"}
ALLOWED_DOC_EXTENSIONS = {"pdf"}


class StorageService:

    def __init__(self):
        self.base_path = Path(settings.FILE_STORAGE_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)

    # ✅ NEW: extension validator
    def _get_extension(self, filename: str) -> str:
        return filename.split(".")[-1].lower()

    def _validate_type(self, file: UploadFile, allowed_types: set, allowed_exts: set):
      content_type = (file.content_type or "").lower().strip()
      extension = file.filename.split(".")[-1].lower()

      if content_type in allowed_types:
        return

      if extension in allowed_exts:
        return

      raise HTTPException(
        400,
        f"Invalid file type: content_type={content_type}, extension={extension}"
    )

    def _validate_size(self, file: UploadFile):
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(400, "File too large")

    def _generate_filename(self, filename: str):
        ext = self._get_extension(filename)
        return f"{uuid.uuid4()}.{ext}"

    def save(self, file: UploadFile, folder: str, allowed_types: set, allowed_exts: set) -> str:
        self._validate_type(file, allowed_types, allowed_exts)
        self._validate_size(file)

        folder_path = self.base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        filename = self._generate_filename(file.filename)
        file_path = folder_path / filename

        try:
            with open(file_path, "wb") as buffer:
                while chunk := file.file.read(1024 * 1024):
                    buffer.write(chunk)

            logger.info(f"File saved: {file_path}")

        except HTTPException:
             raise
        except Exception as e:
            raise HTTPException(500, f"File upload failed: {str(e)}")

        return str(file_path)

    def get(self, path: str):
        file_path = Path(path)
        if not file_path.exists():
            raise HTTPException(404, "File not found")
        return file_path


storage_service = StorageService()