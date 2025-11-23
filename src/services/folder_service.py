from src.exceptions.folder_exceptions import (
    FolderNotFoundError,
    UnexpectedFolderError,
    InvalidFolderParentError,
)
from src.repositories.folder_repository import FolderRepository
from src.models.folder_model import Folder
from src.schemas.folder_schema import FolderCreate, FolderUpdate
from src.core.logger import get_logger

logger = get_logger("FOLDER_SERVICE")


class FolderService:
    def __init__(self, repository: FolderRepository):
        self.repository = repository

    def create_folder(self, data: FolderCreate) -> Folder:
        logger.info("Creating folder with data: %s", data)
        return self.repository.create_folder(data)

    def get_folder(self, folder_id: int) -> Folder:
        logger.info("Fetching folder with ID: %s", folder_id)
        return self.repository.get_folder(folder_id)

    def get_all_folders(self):
        logger.info("Fetching all folders")
        return self.repository.get_all_folders()

    def update_folder(self, folder_id: int, data: FolderUpdate) -> Folder:
        logger.info("Updating folder with ID: %s, data: %s", folder_id, data)
        return self.repository.update_folder(folder_id, data)

    def delete_folder(self, folder_id: int) -> bool:
        logger.info("Deleting folder with ID: %s", folder_id)
        return self.repository.delete_folder(folder_id)

    def get_folder_tree(self, folder_id: int | None = None):
        logger.info("Building folder tree for folder ID: %s", folder_id)
        try:
            if folder_id:
                folder = self.get_folder(folder_id)
                folders_to_build = [folder]
            else:
                folders_to_build = self.repository.get_folders_without_parent()

            def build_tree(f: Folder):
                return {
                    "id": f.id,
                    "name": f.name,
                    "parent_id": f.parent_id,
                    "created_at": f.created_at,
                    "updated_at": f.updated_at,
                    "files": [
                        {
                            "id": file.id,
                            "name": file.name,
                            "extension": file.extension,
                            "created_at": file.created_at,
                        }
                        for file in f.files
                    ],
                    "subfolders": [build_tree(child) for child in f.subfolders],
                }

            return [build_tree(f) for f in folders_to_build]

        except (FolderNotFoundError, InvalidFolderParentError):
            logger.error("Error while building folder tree: %s", folder_id)
            raise
        except Exception as e:
            logger.exception("Unexpected error while building folder tree")
            raise UnexpectedFolderError(
                "Unexpected error while building folder tree"
            ) from e
