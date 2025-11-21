from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import shutil
import os

from src.models.file import File as FileModel
from src.schemas.file import FileCreate, FileUpdate, FileResponse
from src.core.database import get_db
from src.services.file import FileService

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=FileResponse)
def create_file(file: FileCreate, db: Session = Depends(get_db)):
    return FileService.create_file(db, file)


@router.post("/upload/", response_model=FileResponse)
def upload_file(
    folder_id: int = Form(...),
    uploaded_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_location = UPLOAD_DIR / uploaded_file.filename
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    name, extension = os.path.splitext(uploaded_file.filename)
    extension = extension.lstrip(".")

    file_data = FileCreate(name=name, extension=extension, folder_id=folder_id)

    return FileService.create_file(db, file_data)


@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: int, db: Session = Depends(get_db)):
    file = FileService.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.put("/{file_id}", response_model=FileResponse)
def update_file(file_id: int, data: FileUpdate, db: Session = Depends(get_db)):
    file = FileService.update_file(db, file_id, data)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.delete("/{file_id}", response_model=dict)
def delete_file(file_id: int, db: Session = Depends(get_db)):
    success = FileService.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"deleted": success}


@router.get("/folder/{folder_id}", response_model=List[FileResponse])
def get_files_in_folder(folder_id: int, db: Session = Depends(get_db)):
    return FileService.get_files_in_folder(db, folder_id)
