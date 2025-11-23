from typing import Optional
from fastapi import UploadFile

from src.repositories.file_repository import FileRepository
from src.models.file_model import File as FileModel
from src.schemas.file_schema import FileCreate, FileUpdate
from src.core.logger import get_logger

logger = get_logger("FILE_SERVICE")


class FileService:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def create_file(self, data: FileCreate) -> FileModel:
        logger.info("Creating file with data: %s", data)
        return self.repository.create_file(data)

    def get_file(self, file_id: int) -> Optional[FileModel]:
        logger.info("Fetching file with ID: %s", file_id)
        return self.repository.get_file(file_id)

    def update_file(self, file_id: int, data: FileUpdate) -> Optional[FileModel]:
        logger.info("Updating file with ID: %s, data: %s", file_id, data)
        return self.repository.update_file(file_id, data)

    def delete_file(self, file_id: int) -> bool:
        logger.info("Deleting file with ID: %s", file_id)
        return self.repository.delete_file(file_id)

    def get_files_in_folder(self, folder_id: int):
        logger.info("Fetching files in folder with ID: %s", folder_id)
        return self.repository.get_files_in_folder(folder_id)

    def upload_file(self, folder_id: int, file: UploadFile) -> FileModel:
        logger.info("Uploading file: %s to folder ID: %s", file.filename, folder_id)
        return self.repository.upload_file(folder_id, file)
