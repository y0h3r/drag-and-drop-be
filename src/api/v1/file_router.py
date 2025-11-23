from fastapi import APIRouter, Depends, File, UploadFile, Form
from typing import List
from pathlib import Path
import shutil
import os

from src.core.logger import get_logger
from src.providers.services.file_service_provider import get_file_service
from src.schemas.file_schema import FileCreate, FileUpdate, FileResponse
from src.services.file_service import FileService

router = APIRouter(prefix="/files", tags=["Files"])
logger = get_logger("FILE_ROUTER")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=FileResponse)
def create_file(file: FileCreate, service: FileService = Depends(get_file_service)):
    logger.info("Creating a new file with data: %s", file)
    return service.create_file(file)


@router.post("/upload/", response_model=FileResponse)
def upload_file(
    folder_id: int = Form(...),
    uploaded_file: UploadFile = File(...),
    service: FileService = Depends(get_file_service),
):
    logger.info(
        "Uploading file: %s to folder ID: %s", uploaded_file.filename, folder_id
    )
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_location = UPLOAD_DIR / uploaded_file.filename
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    name, extension = os.path.splitext(uploaded_file.filename)
    extension = extension.lstrip(".")

    file_data = FileCreate(name=name, extension=extension, folder_id=folder_id)

    return service.upload_file(folder_id, file_data)


@router.get("/{file_id}", response_model=FileResponse)
def get_file(
    file_id: int,
    service: FileService = Depends(get_file_service),
):
    logger.info("Fetching file with ID: %s", file_id)
    return service.get_file(file_id)


@router.put("/{file_id}", response_model=FileResponse)
def update_file(
    file_id: int,
    data: FileUpdate,
    service: FileService = Depends(get_file_service),
):
    logger.info("Updating file with ID: %s, data: %s", file_id, data)
    return service.update_file(file_id, data)


@router.delete("/{file_id}", response_model=dict)
def delete_file(file_id: int, service: FileService = Depends(get_file_service)):
    logger.info("Deleting file with ID: %s", file_id)
    return service.delete_file(file_id)


@router.get("/folder/{folder_id}", response_model=List[FileResponse])
def get_files_in_folder(
    folder_id: int, service: FileService = Depends(get_file_service)
):
    logger.info("Fetching all files in folder with ID: %s", folder_id)
    return service.get_files_in_folder(folder_id)
