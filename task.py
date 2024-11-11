from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from sqlalchemy.orm import Session
from models import Task

OPTIONS = ['Title', 'Description', 'Complete', 'Incomplete']

console = Console()

def get_task_by_id(session: Session, id: int) -> Task:
    task = session.query(Task).filter(Task.id == id).first()

    if not task: 
        console.print(f"[bold red]Error:[/bold red] [red]Task with id [bold]{id}[/bold] not found[/red]")
        return
    
    return task

def get_all_tasks(session: Session) -> list[Task]:
    return session.query(Task).all()


def create_task(session: Session, title: str, description: str) -> None:
    task = Task(title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    console.print(task)

def delete_task(session: Session, id: int, interactive: bool = False) -> None:
    task = get_task_by_id(session, id)
    if not task:
        return
    
    if interactive:
        if not Confirm.ask(f"Do you want to delete: [yellow]{task.id}-[/yellow] [bold]{task.title}[/bold]?"):
            console.print("[bold red] Deletion Cancelled [/bold red]")
            return
        
    session.delete(task)
    console.print(task)
    session.commit()
    

def update_task(session: Session, id: int, message: str, title: str = None, description: str = None, completed: bool = None, ) -> None:
    task = get_task_by_id(session, id)

    if not task:
        return

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed

    session.commit() 
    session.refresh(task)
    console.print(task)

def complete_task(session: Session, id: int) -> None:
    update_task(session, id, "Marked As Completed ✔️", completed=True)

def list_tasks(session: Session) -> None:
    tasks = get_all_tasks(session)

    if not tasks:
        console.print("\n\t[magenta] No Tasks have been created yet[/magenta]\n")
        return

    table = Table(title="All Tasks 📃\n", show_edge=False, leading = True, title_style="bold")
    table.add_column("Id")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Completed")

    for task in tasks:
        table.add_row(str(task.id), task.title, task.description, task.render_completed())
    console.print(table)