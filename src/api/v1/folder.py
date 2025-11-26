from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.folder import FolderCreate, FolderUpdate, FolderResponse, FolderTree
from src.core.database import get_db
from src.services.folder import FolderService

router = APIRouter(prefix="/folders", tags=["Folders"])


@router.post("/", response_model=FolderResponse)
async def create_folder(folder: FolderCreate, db: AsyncSession = Depends(get_db)):
    return await FolderService.create_folder(db, folder)


@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder(folder_id: int, db: AsyncSession = Depends(get_db)):
    folder = await FolderService.get_folder(db, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


@router.get("/", response_model=List[FolderTree])
async def list_folders(db: AsyncSession = Depends(get_db)):
    return await FolderService.get_folder_tree(db)


@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: int, data: FolderUpdate, db: AsyncSession = Depends(get_db)
):
    folder = await FolderService.update_folder(db, folder_id, data)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


@router.delete("/{folder_id}", response_model=dict)
async def delete_folder(folder_id: int, db: AsyncSession = Depends(get_db)):
    success = await FolderService.delete_folder(db, folder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Folder not found")
    return {"deleted": success}
