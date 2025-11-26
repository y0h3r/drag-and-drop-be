import os
from typing import Optional, List
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.file import File as FileModel
from src.models.folder import Folder
from src.schemas.file import FileCreate, FileUpdate

UPLOAD_DIR = "uploads"


class FileService:

    @staticmethod
    async def create_file(db: AsyncSession, data: FileCreate) -> FileModel:
        result = await db.execute(select(Folder).where(Folder.id == data.folder_id))
        folder = result.scalars().first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder does not exist")

        file = FileModel(
            name=data.name, extension=data.extension, folder_id=data.folder_id
        )
        db.add(file)
        await db.commit()
        await db.refresh(file)
        return file

    @staticmethod
    async def get_file(db: AsyncSession, file_id: int) -> Optional[FileModel]:
        result = await db.execute(select(FileModel).where(FileModel.id == file_id))
        return result.scalars().first()

    @staticmethod
    async def update_file(
        db: AsyncSession, file_id: int, data: FileUpdate
    ) -> Optional[FileModel]:
        file = await FileService.get_file(db, file_id)
        if not file:
            return None

        if data.name is not None:
            file.name = data.name
        if data.folder_id is not None:
            file.folder_id = data.folder_id

        await db.commit()
        await db.refresh(file)
        return file

    @staticmethod
    async def delete_file(db: AsyncSession, file_id: int) -> bool:
        file = await FileService.get_file(db, file_id)
        if not file:
            return False

        await db.delete(file)
        await db.commit()
        return True

    @staticmethod
    async def get_files_in_folder(db: AsyncSession, folder_id: int) -> List[FileModel]:
        result = await db.execute(
            select(FileModel).where(FileModel.folder_id == folder_id)
        )
        return result.scalars().all()

    @staticmethod
    async def upload_file(
        db: AsyncSession, folder_id: int, uploaded_file: UploadFile
    ) -> FileModel:
        import aiofiles

        result = await db.execute(select(Folder).where(Folder.id == folder_id))
        folder = result.scalars().first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder does not exist")

        # Solo PDF
        if not uploaded_file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)

        async with aiofiles.open(file_path, "wb") as out_file:
            content = await uploaded_file.read()
            await out_file.write(content)

        new_file = FileModel(
            name=uploaded_file.filename.replace(".pdf", ""),
            extension="pdf",
            folder_id=folder_id,
        )

        db.add(new_file)
        await db.commit()
        await db.refresh(new_file)
        return new_file
