from fastapi import Depends
from src.providers.repositories.folder_repository_provider import get_folder_repository
from src.services.folder_service import FolderService
from src.repositories.folder_repository import FolderRepository


def get_folder_service(repo: FolderRepository = Depends(get_folder_repository)):
    return FolderService(repo)
