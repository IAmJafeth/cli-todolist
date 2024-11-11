from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from sqlalchemy.orm import Session
from models import Task

OPTIONS = ['Title', 'Description']
COMPLETE_SYMBOL = '✅'
INCOMPLETE_SYMBOL = '❌'

console = Console()

def get_all_tasks(session: Session) -> list[Task]:
    return session.query(Task).all()

def render_completed(completed: bool, complete_symbol: str = COMPLETE_SYMBOL, incomplete_symbol: str = INCOMPLETE_SYMBOL) -> str:
    return complete_symbol if completed else incomplete_symbol

def print_task(task: Task, message: str = "Details"):
    table = Table(title=f"Task {task.id} {message}\n", show_edge=False, show_header=False, title_style="b")
    table.add_column(justify="right")
    table.add_column( justify="left")

    table.add_row("Id", str(task.id))
    table.add_row("Title", task.title)
    if task.description: table.add_row("Description", task.description)
    table.add_row("Complete", render_completed(task.completed))

    console.print(table)

def create_task(session: Session, title: str, description: str) -> None:
    task = Task(title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    print_task(task, "Created Successfully ☀️")

def delete_task(session: Session, id: int, interactive: bool = False) -> None:
    task = session.query(Task).filter(Task.id == id).first()
    if task:
        if interactive:
            if not Confirm.ask(f"Do you want to delete: [yellow]{task.id}-[/yellow] [bold]{task.title}[/bold]?"):
                console.print("[bold red] Deletion Cancelled [/bold red]")
                return
            
        session.delete(task)
        print_task(task, "Deleted Succesfully 🚮")
        session.commit()
    else:
        console.print(f"[bold red]Delete Error:[/bold red] [red]Task with id [bold]{id}[/bold] not found[/red]")

def update_task(session: Session, id: int, message: str, title: str = None, description: str = None, completed: bool = None, ) -> None:
    task = session.query(Task).filter(Task.id == id).first()
    if not task:
        console.print(f"[bold red]Delete Error:[/bold red] [red]Task with id [bold]{id}[/bold] not found[/red]")
        return

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed

    session.commit() 
    session.refresh(task)
    print_task(task, message)

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
        table.add_row(str(task.id), task.title, task.description, render_completed(task.completed))
    console.print(table)