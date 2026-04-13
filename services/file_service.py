from fastapi import UploadFile
from core.storage import (
    storage_service,
    ALLOWED_IMAGE_TYPES,
    ALLOWED_DOC_TYPES,
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_DOC_EXTENSIONS
)


class FileService:

    @staticmethod
    def upload_profile_image(file: UploadFile) -> str:
        return storage_service.save(file, "profile_images", ALLOWED_IMAGE_TYPES, ALLOWED_IMAGE_EXTENSIONS)

    @staticmethod
    def upload_passport(file: UploadFile) -> str:
        return storage_service.save(
            file,
            "passport_files",
            ALLOWED_DOC_TYPES,
            ALLOWED_DOC_EXTENSIONS
        )