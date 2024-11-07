from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from typing import Optional

Base = declarative_base()

class Task(Base):
    __tablename__ = "task"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column( String(30), nullable=False)
    description: Mapped[Optional[str]]
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self):
        return f"<task.Task(id={self.id}, title={self.title}, description={self.description}, completed={self.completed})>"
