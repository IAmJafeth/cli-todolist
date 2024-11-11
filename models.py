from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from typing import Optional
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

Base = declarative_base()

class Task(Base):
    __tablename__ = "task"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column( String(30), nullable=False)
    description: Mapped[Optional[str]]
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)

    def render_completed(self) -> str:
        return '✅' if self.completed else '❌'

    def __repr__(self) -> str:
        return f"<task.Task(id={self.id}, title={self.title}, description={self.description}, completed={self.completed})>"

    def __rich_console__(self, console: Console, otions: ConsoleOptions)-> RenderResult :
        table = Table(title=f"Task {self.id} Details \n", show_edge=False, show_header=False, title_style="b")
        table.add_column(justify="right")
        table.add_column( justify="left")

        table.add_row("Id", str(self.id))
        table.add_row("Title", self.title)
        if self.description: table.add_row("Description", self.description)
        table.add_row("Complete", self.render_completed())

        yield table