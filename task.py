from typing import Dict, Union
from rich.table import Table
from rich.console import Console

console = Console()

class Task:
    tasks: Dict[int, "Task"] = {}
    __current_id: int = 0

    def __init__(self, title: str, description:Union[str, None] = None) -> None:
        self.id = Task.__current_id
        self.title = title
        self.description = description
        self.completed = False

    def __repr__(self) -> str:
        return f"<task.Task(id={self.id}, title={self.title}, description={self.description}, completed={self.completed})>"

    def render_completed(self, complete_symbol: str = '✅', incomplete_symbol: str = '❌') -> str:
        return complete_symbol if self.completed else incomplete_symbol

    def show_details(self,description: str = "Details") -> None:
        table = Table(title=f"\nTask {self.id} {description}\n", show_edge=False)

        table.add_column("Field", justify="right")
        table.add_column("Value", justify="left")

        table.add_row("Id", str(self.id))
        table.add_row("Title", self.title)
        if self.description: table.add_row("Description", self.description)
        table.add_row("Complete", self.render_completed())

        console.print(table)

    @classmethod
    def create(cls, title: str, description:str) -> "Task":
        task = Task(title,description)
        cls.tasks[task.id] = task
        cls.__current_id += 1
        return task
    
    @classmethod
    def delete(cls, id:int) -> Union[bool,"Task"]:
        if id in cls.tasks:
            task = cls.tasks[id]
            del cls.tasks[id]
            return task
        return False
    
    @classmethod
    def complete(cls, id:int) -> Union[bool,"Task"]:
        if id in cls.tasks:
            cls.tasks[id].completed = True
            return cls.tasks[id]
        return False

    @classmethod
    def list_all(cls) -> None:
        if  not cls.tasks:
            print("\nNo Tasks have been created yet")
            return
        table = Table(title="\nCurrent Tasks\n", show_edge=False)
        table.add_column("Id")
        table.add_column("Title")
        table.add_column("Description")
        table.add_column("Completed")

        for task in cls.tasks.values():
            table.add_row(str(task.id), task.title, task.description, task.render_completed())

        console.print(table)

