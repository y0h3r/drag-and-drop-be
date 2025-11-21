from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.schemas.folder import FolderCreate, FolderUpdate, FolderResponse, FolderTree
from src.core.database import get_db
from src.services.folder import FolderService

router = APIRouter(prefix="/folders", tags=["Folders"])


@router.post("/", response_model=FolderResponse)
def create_folder(folder: FolderCreate, db: Session = Depends(get_db)):
    return FolderService.create_folder(db, folder)


@router.get("/{folder_id}", response_model=FolderResponse)
def get_folder(folder_id: int, db: Session = Depends(get_db)):
    folder = FolderService.get_folder(db, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


@router.get("/", response_model=List[FolderTree])
def list_folders(db: Session = Depends(get_db)):
    return FolderService.get_folder_tree(db)


@router.put("/{folder_id}", response_model=FolderResponse)
def update_folder(folder_id: int, data: FolderUpdate, db: Session = Depends(get_db)):
    folder = FolderService.update_folder(db, folder_id, data)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


@router.delete("/{folder_id}", response_model=dict)
def delete_folder(folder_id: int, db: Session = Depends(get_db)):
    success = FolderService.delete_folder(db, folder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Folder not found")
    return {"deleted": success}
