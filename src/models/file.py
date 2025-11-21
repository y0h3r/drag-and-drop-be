from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Integer, DateTime, func

from src.core.database import Base


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    extension: Mapped[str] = mapped_column(String(10), nullable=False)

    folder_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("folders.id", ondelete="CASCADE"),
        nullable=False
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

    folder: Mapped["Folder"] = relationship("Folder", back_populates="files")
