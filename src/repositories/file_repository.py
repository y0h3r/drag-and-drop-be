import os
from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.models.folder_model import Folder
from src.schemas.file_schema import FileCreate, FileUpdate
from src.models.file_model import File as FileModel
from src.exceptions.file_exceptions import (
    FolderNotFoundError,
    FileNotFoundError,
    InvalidFileTypeError,
)
from src.core.logger import get_logger

UPLOAD_DIR = "uploads"
logger = get_logger("FILE_REPOSITORY")


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_file(self, data: FileCreate) -> FileModel:
        logger.info(
            "Creating file in folder ID: %s with data: %s", data.folder_id, data
        )
        folder = self.db.query(Folder).filter(Folder.id == data.folder_id).first()
        if not folder:
            logger.error("Folder not found for ID: %s", data.folder_id)
            raise FolderNotFoundError("Folder does not exist")

        file = FileModel(
            name=data.name,
            extension=data.extension,
            folder_id=data.folder_id,
        )
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        logger.info("File created with ID: %s", file.id)
        return file

    def get_file(self, file_id: int) -> Optional[FileModel]:
        logger.info("Fetching file with ID: %s", file_id)
        file = self.db.query(FileModel).filter(FileModel.id == file_id).first()
        if not file:
            logger.error("File not found for ID: %s", file_id)
            raise FileNotFoundError("File not found")
        return file

    def update_file(self, file_id: int, data: FileUpdate) -> FileModel:
        logger.info("Updating file with ID: %s, data: %s", file_id, data)
        file = self.get_file(file_id)

        if data.name is not None:
            file.name = data.name

        if data.folder_id is not None:
            file.folder_id = data.folder_id

        self.db.commit()
        self.db.refresh(file)
        logger.info("File updated with ID: %s", file.id)
        return file

    def delete_file(self, file_id: int) -> bool:
        logger.info("Deleting file with ID: %s", file_id)
        file = self.get_file(file_id)

        self.db.delete(file)
        self.db.commit()
        logger.info("File deleted with ID: %s", file_id)
        return True

    def get_files_in_folder(self, folder_id: int):
        logger.info("Fetching files in folder with ID: %s", folder_id)
        folder = self.db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            logger.error("Folder not found for ID: %s", folder_id)
            raise FolderNotFoundError("Folder does not exist")

        return self.db.query(FileModel).filter(FileModel.folder_id == folder_id).all()

    def upload_file(self, folder_id: int, file: UploadFile) -> FileModel:
        logger.info("Uploading file: %s to folder ID: %s", file.filename, folder_id)
        folder = self.db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            logger.error("Folder not found for ID: %s", folder_id)
            raise FolderNotFoundError("Folder does not exist")

        if not file.filename.lower().endswith(".pdf"):
            logger.error("Invalid file type for file: %s", file.filename)
            raise InvalidFileTypeError("Only PDF files are allowed")

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        new_file = FileModel(
            name=file.filename.replace(".pdf", ""),
            extension="pdf",
            folder_id=folder_id,
        )

        self.db.add(new_file)
        self.db.commit()
        self.db.refresh(new_file)
        logger.info("File uploaded with ID: %s", new_file.id)
        return new_file
