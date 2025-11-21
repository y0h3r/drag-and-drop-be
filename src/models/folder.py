from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Integer, DateTime, func

from src.core.database import Base


class Folder(Base):
    __tablename__ = "folders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("folders.id", ondelete="CASCADE"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    parent: Mapped["Folder"] = relationship(
        "Folder",
        remote_side="Folder.id",
        back_populates="subfolders"
    )

    subfolders: Mapped[list["Folder"]] = relationship(
        "Folder",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="folder",
        cascade="all, delete-orphan"
    )
