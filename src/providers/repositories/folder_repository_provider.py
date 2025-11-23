from sqlalchemy.orm import Session
from fastapi import Depends
from src.core.database import get_db
from src.repositories.folder_repository import FolderRepository


def get_folder_repository(db: Session = Depends(get_db)):
    return FolderRepository(db)
