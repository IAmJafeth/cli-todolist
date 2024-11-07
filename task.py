from rich.table import Table
from rich.console import Console
from database import Session
from models import Task

console = Console()

def render_completed(completed: bool, complete_symbol: str = '✅', incomplete_symbol: str = '❌') -> str:
    return complete_symbol if completed else incomplete_symbol

def print_task(task: Task, message: str = "Details"):
    table = Table(title=f"\nTask {task.id} {message}\n", show_edge=False, show_header=False)
    table.add_column(justify="right")
    table.add_column( justify="left")

    table.add_row("Id", str(task.id))
    table.add_row("Title", task.title)
    if task.description: table.add_row("Description", task.description)
    table.add_row("Complete", render_completed(task.completed))

    console.print(table)

def create_task(title: str, description: str) -> None:
    with Session() as session:
        task = Task(title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        print_task(task, "Created Successfully ☀️")

def delete_task(id: int) -> None:
    with Session() as session:
        task = session.query(Task).filter(Task.id == id).first()
        if task:
            session.delete(task)
            print_task(task, "Deleted Succesfully 🚮")
            session.commit()
        else:
            console.print(f"[bold red]Delete Error:[/bold red] [red]Task with id [bold]{id}[/bold] not found[/red]")

def update_task(id: int, message: str, title: str = None, description: str = None, completed: bool = None, ) -> None:
    with Session() as session:
        task = session.query(Task).filter(Task.id == id).first()
        if not task:
            console.print(f"[bold red]Delete Error:[/bold red] [red]Task with id [bold]{id}[/bold] not found[/red]")
            return

        # Update fields if new values are provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        session.commit()  # Save changes to the database
        session.refresh(task)  # Refresh the instance to ensure it's up-to-date
        print_task(task, message)

def complete_task(id: int) -> None:
    update_task(id, "Marked As Completed ✔️", completed=True)

def get_all_tasks() -> list[Task]:
    with Session() as session:
        return session.query(Task).all()

def list_tasks() -> None:
    tasks = get_all_tasks()

    if not tasks:
        console.print("\n\t[magenta] No Tasks have been created yet[/magenta]\n")
        return

    table = Table(title="\nAll Tasks 📃\n", show_edge=False)
    table.add_column("Id")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Completed")

    for task in tasks:
        table.add_row(str(task.id), task.title, task.description, render_completed(task.completed))

    console.print(table)