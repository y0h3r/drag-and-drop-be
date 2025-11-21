from sqlalchemy.orm import Session
from src.models.folder import Folder
from src.schemas.folder import FolderCreate, FolderUpdate


class FolderService:

    @staticmethod
    def create_folder(db: Session, data: FolderCreate) -> Folder:
        folder = Folder(name=data.name, parent_id=data.parent_id)
        db.add(folder)
        db.commit()
        db.refresh(folder)
        return folder

    @staticmethod
    def get_folder(db: Session, folder_id: int) -> Folder | None:
        return db.query(Folder).filter(Folder.id == folder_id).first()

    @staticmethod
    def get_all_folders(db: Session):
        return db.query(Folder).all()

    @staticmethod
    def update_folder(db: Session, folder_id: int, data: FolderUpdate) -> Folder | None:
        folder = FolderService.get_folder(db, folder_id)
        if not folder:
            return None

        if data.name is not None:
            folder.name = data.name

        if data.parent_id is not None:
            folder.parent_id = data.parent_id

        db.commit()
        db.refresh(folder)
        return folder

    @staticmethod
    def delete_folder(db: Session, folder_id: int) -> bool:
        folder = FolderService.get_folder(db, folder_id)
        if not folder:
            return False

        db.delete(folder)
        db.commit()
        return True

    @staticmethod
    def get_folder_tree(db: Session, folder_id: int | None = None):
        """Recursive tree builder."""
        if folder_id:
            # Construye árbol desde un folder específico
            folder = FolderService.get_folder(db, folder_id)
            if not folder:
                return None
            folders_to_build = [folder]
        else:
            # Construye árbol desde los folders raíz
            folders_to_build = db.query(Folder).filter(Folder.parent_id == None).all()

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
