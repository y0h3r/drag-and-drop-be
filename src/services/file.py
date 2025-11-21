import os
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile

from src.models.file import File as FileModel
from src.models.folder import Folder
from src.schemas.file import FileCreate, FileUpdate


UPLOAD_DIR = "uploads"


class FileService:
    @staticmethod
    def create_file(db: Session, data: FileCreate) -> FileModel:
        folder = db.query(Folder).filter(Folder.id == data.folder_id).first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder does not exist")

        file = FileModel(
            name=data.name,
            extension=data.extension,
            folder_id=data.folder_id,
        )
        db.add(file)
        db.commit()
        db.refresh(file)
        return file

    @staticmethod
    def get_file(db: Session, file_id: int) -> Optional[FileModel]:
        return db.query(FileModel).filter(FileModel.id == file_id).first()

    @staticmethod
    def update_file(db: Session, file_id: int, data: FileUpdate) -> Optional[FileModel]:
        file = FileService.get_file(db, file_id)
        if not file:
            return None

        if data.name is not None:
            file.name = data.name

        if data.folder_id is not None:
            file.folder_id = data.folder_id

        db.commit()
        db.refresh(file)
        return file

    @staticmethod
    def delete_file(db: Session, file_id: int) -> bool:
        file = FileService.get_file(db, file_id)
        if not file:
            return False

        db.delete(file)
        db.commit()
        return True

    @staticmethod
    def get_files_in_folder(db: Session, folder_id: int):
        return db.query(FileModel).filter(FileModel.folder_id == folder_id).all()

    @staticmethod
    def upload_file(db: Session, folder_id: int, file: UploadFile) -> FileModel:
        folder = db.query(Folder).filter(Folder.id == folder_id).first()
        if not folder:
            raise ValueError("Folder does not exist")

        if not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are allowed")

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        new_file = FileModel(
            name=file.filename.replace(".pdf", ""),
            extension="pdf",
            folder_id=folder_id,
        )

        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        return new_file
