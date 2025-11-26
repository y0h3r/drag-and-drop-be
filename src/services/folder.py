from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.folder import Folder
from src.schemas.folder import FolderCreate, FolderUpdate


class FolderService:

    @staticmethod
    async def create_folder(db: AsyncSession, data: FolderCreate) -> Folder:
        folder = Folder(name=data.name, parent_id=data.parent_id)
        db.add(folder)
        await db.commit()
        await db.refresh(folder)
        return folder

    @staticmethod
    async def get_folder(db: AsyncSession, folder_id: int) -> Optional[Folder]:
        result = await db.execute(
            select(Folder)
            .options(
                selectinload(Folder.files),
                selectinload(Folder.subfolders).selectinload(Folder.files),
            )
            .where(Folder.id == folder_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_all_folders(db: AsyncSession) -> List[Folder]:
        result = await db.execute(
            select(Folder).options(
                selectinload(Folder.files),
                selectinload(Folder.subfolders).selectinload(Folder.files),
            )
        )
        return result.scalars().all()

    @staticmethod
    async def update_folder(
        db: AsyncSession, folder_id: int, data: FolderUpdate
    ) -> Optional[Folder]:
        folder = await FolderService.get_folder(db, folder_id)
        if not folder:
            return None

        if data.name is not None:
            folder.name = data.name
        if data.parent_id is not None:
            folder.parent_id = data.parent_id

        await db.commit()
        await db.refresh(folder)
        return folder

    @staticmethod
    async def delete_folder(db: AsyncSession, folder_id: int) -> bool:
        folder = await FolderService.get_folder(db, folder_id)
        if not folder:
            return False

        await db.delete(folder)
        await db.commit()
        return True

    @staticmethod
    async def get_folder_tree(db: AsyncSession, folder_id: Optional[int] = None):
        """Recursive tree builder loading everything in a single query."""
        query = select(Folder).options(
            selectinload(Folder.files),
            selectinload(Folder.subfolders).selectinload(Folder.files),
        )

        if folder_id:
            query = query.where(Folder.id == folder_id)
        else:
            query = query.where(Folder.parent_id == None)

        result = await db.execute(query)
        folders_to_build = result.scalars().all()

        def build_tree(f: Folder):
            return {
                "id": f.id,
                "name": f.name,
                "parent_id": f.parent_id,
                "created_at": f.created_at,
                "updated_at": f.updated_at,
                "files": [
                    {
                        "id": file.id,
                        "name": file.name,
                        "extension": file.extension,
                        "created_at": file.created_at,
                    }
                    for file in f.files
                ],
                "subfolders": [build_tree(child) for child in f.subfolders],
            }

        return [build_tree(f) for f in folders_to_build]
