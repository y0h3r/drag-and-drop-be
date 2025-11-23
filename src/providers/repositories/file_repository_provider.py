from sqlalchemy.orm import Session
from fastapi import Depends
from src.core.database import get_db
from src.repositories.file_repository import FileRepository


def get_file_repository(db: Session = Depends(get_db)):
    return FileRepository(db)
