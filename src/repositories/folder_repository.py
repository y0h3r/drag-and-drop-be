from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.models.folder_model import Folder
from src.schemas.folder_schema import FolderCreate, FolderUpdate
from src.exceptions.folder_exceptions import (
    FolderNotFoundError,
    InvalidFolderParentError,
    UnexpectedFolderError,
)
from src.core.logger import get_logger

logger = get_logger("FOLDER_REPOSITORY")


class FolderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_folder(self, data: FolderCreate) -> Folder:
        logger.info("Creating folder with data: %s", data)
        try:
            folder = Folder(name=data.name, parent_id=data.parent_id)
            self.db.add(folder)
            self.db.commit()
            self.db.refresh(folder)
            logger.info("Folder created with ID: %s", folder.id)
            return folder
        except SQLAlchemyError as ex:
            logger.exception("Unexpected error creating folder")
            raise UnexpectedFolderError(f"Unexpected error creating folder: {ex}")

    def get_folder(self, folder_id: int) -> Folder:
        logger.info("Fetching folder with ID: %s", folder_id)
        folder = self.db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            logger.error("Folder not found for ID: %s", folder_id)
            raise FolderNotFoundError(f"Folder {folder_id} was not found")
        return folder

    def get_all_folders(self):
        logger.info("Fetching all folders")
        try:
            return self.db.query(Folder).all()
        except SQLAlchemyError as ex:
            logger.exception("Error fetching folders")
            raise UnexpectedFolderError(f"Error fetching folders: {ex}")

    def update_folder(self, folder_id: int, data: FolderUpdate) -> Folder:
        logger.info("Updating folder with ID: %s, data: %s", folder_id, data)
        folder = self.get_folder(folder_id)

        if data.parent_id is not None and data.parent_id == folder.id:
            logger.error("Invalid parent ID for folder: %s", folder_id)
            raise InvalidFolderParentError("A folder cannot be its own parent")

        try:
            if data.name is not None:
                folder.name = data.name

            if data.parent_id is not None:
                folder.parent_id = data.parent_id

            self.db.commit()
            self.db.refresh(folder)
            logger.info("Folder updated with ID: %s", folder.id)
            return folder

        except SQLAlchemyError as ex:
            logger.exception("Unexpected error updating folder")
            raise UnexpectedFolderError(f"Unexpected error updating folder: {ex}")

    def delete_folder(self, folder_id: int) -> bool:
        logger.info("Deleting folder with ID: %s", folder_id)
        folder = self.get_folder(folder_id)

        try:
            self.db.delete(folder)
            self.db.commit()
            logger.info("Folder deleted with ID: %s", folder_id)
            return True
        except SQLAlchemyError as ex:
            logger.exception("Unexpected error deleting folder")
            raise UnexpectedFolderError(f"Unexpected error deleting folder: {ex}")

    def get_folders_without_parent(self):
        logger.info("Fetching folders without parent")
        try:
            return self.db.query(Folder).filter(Folder.parent_id == None).all()
        except SQLAlchemyError as ex:
            logger.exception("Unexpected error fetching folders without parent")
            raise UnexpectedFolderError(f"Unexpected error fetching folders: {ex}")
