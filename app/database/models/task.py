from app.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, func, ForeignKey
from datetime import datetime


class TaskTable(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    description: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now, nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    completed: Mapped[bool] = mapped_column(default=False, index=True, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["UserTable"] = relationship(back_populates="tasks")
