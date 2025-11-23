from fastapi import APIRouter, Depends
from typing import List

from src.core.logger import get_logger
from src.providers.services.folder_service_provider import get_folder_service
from src.schemas.folder_schema import (
    FolderCreate,
    FolderUpdate,
    FolderResponse,
    FolderTree,
)
from src.services.folder_service import FolderService

router = APIRouter(prefix="/folders", tags=["Folders"])
logger = get_logger("FILE_ROUTER")


@router.post("/", response_model=FolderResponse)
def create_folder(
    folder: FolderCreate, service: FolderService = Depends(get_folder_service)
):
    logger.info("Creating a new folder with data: %s", folder)
    return service.create_folder(folder)


@router.get("/{folder_id}", response_model=FolderResponse)
def get_folder(folder_id: int, service: FolderService = Depends(get_folder_service)):
    logger.info("Fetching folder with ID: %s", folder_id)
    return service.get_folder(folder_id)


@router.get("/", response_model=List[FolderTree])
def list_folders(service: FolderService = Depends(get_folder_service)):
    logger.info("Fetching folder tree for all folders")
    return service.get_folder_tree()


@router.put("/{folder_id}", response_model=FolderResponse)
def update_folder(
    folder_id: int,
    data: FolderUpdate,
    service: FolderService = Depends(get_folder_service),
):
    logger.info("Updating folder with ID: %s, data: %s", folder_id, data)
    return service.update_folder(folder_id, data)


@router.delete("/{folder_id}", response_model=dict)
def delete_folder(folder_id: int, service: FolderService = Depends(get_folder_service)):
    logger.info("Deleting folder with ID: %s", folder_id)
    return service.delete_folder(folder_id)
