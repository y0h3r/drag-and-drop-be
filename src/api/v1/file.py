from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.file import FileCreate, FileUpdate, FileResponse
from src.core.database import get_db
from src.services.file import FileService

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/", response_model=FileResponse)
async def create_file(file: FileCreate, db: AsyncSession = Depends(get_db)):
    return await FileService.create_file(db, file)


@router.post("/upload/", response_model=FileResponse)
async def upload_file(
    folder_id: int = Form(...),
    uploaded_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await FileService.upload_file(db, folder_id, uploaded_file)


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(file_id: int, db: AsyncSession = Depends(get_db)):
    file = await FileService.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.put("/{file_id}", response_model=FileResponse)
async def update_file(
    file_id: int, data: FileUpdate, db: AsyncSession = Depends(get_db)
):
    file = await FileService.update_file(db, file_id, data)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.delete("/{file_id}", response_model=dict)
async def delete_file(file_id: int, db: AsyncSession = Depends(get_db)):
    success = await FileService.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"deleted": success}


@router.get("/folder/{folder_id}", response_model=List[FileResponse])
async def get_files_in_folder(folder_id: int, db: AsyncSession = Depends(get_db)):
    return await FileService.get_files_in_folder(db, folder_id)
