from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class FolderBase(BaseModel):
    name: str = Field(..., example="Financial Documents")


class FolderCreate(FolderBase):
    parent_id: Optional[int] = Field(
        None, description="ID of parent folder for nesting"
    )


class FolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class FolderResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FileInFolder(BaseModel):
    id: int
    name: str
    extension: str
    created_at: datetime

    class Config:
        from_attributes = True


class FolderTree(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    files: List[FileInFolder] = []
    subfolders: List["FolderTree"] = []

    class Config:
        from_attributes = True


FolderTree.update_forward_refs()
