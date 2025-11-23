from fastapi import Depends
from src.repositories.file_repository import FileRepository
from src.providers.repositories.file_repository_provider import get_file_repository
from src.services.file_service import FileService


def get_file_service(repo: FileRepository = Depends(get_file_repository)):
    return FileService(repo)
