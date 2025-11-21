from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class FileBase(BaseModel):
    name: str = Field(..., example="Report")
    extension: str = Field(..., example="pdf")


class FileCreate(FileBase):
    folder_id: int = Field(..., description="Folder where the file is stored")

    @field_validator("extension")
    @classmethod
    def only_pdf(cls, ext: str) -> str:
        if ext.lower() != "pdf":
            raise ValueError("Only PDF files are allowed")
        return ext.lower()


class FileUpdate(BaseModel):
    name: Optional[str] = None
    extension: Optional[str] = None
    folder_id: Optional[int]

    @field_validator("extension")
    @classmethod
    def extension_not_allowed(cls, ext: Optional[str]) -> Optional[str]:
        if ext is not None:
            raise ValueError("File extension cannot be modified")
        return ext


class FileResponse(BaseModel):
    id: int
    name: str
    extension: str
    folder_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
