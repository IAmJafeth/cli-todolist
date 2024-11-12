from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from sqlalchemy.orm import Session
from models import Task

console = Console()

def get_task_by_id(session: Session, id: int) -> Task:
    task = session.query(Task).filter(Task.id == id).first()

    if not task: 
        console.print(f"[bold red]Error:[/bold red] [red]Task with id [yellow bold]{id}[/yellow bold] not found ×[/red]")
        return
    
    return task

def get_all_tasks(session: Session, order_by: str = 'id', reveresed_flag: bool = False) -> list[Task]:
    tasks = session.query(Task).order_by(getattr(Task,order_by)).all()
    return tasks if not reveresed_flag else list(reversed(tasks))


def create_task(session: Session, title: str, description: str) -> bool:
    task = Task(title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    console.print(task, f"\n[green]Task [bold]{task.id}[/bold] created successfully ✔[/green]")
    return True

def delete_task(session: Session, id: int, interactive: bool = False) -> bool:
    task = get_task_by_id(session, id)
    if not task:
        return False
    
    if interactive:
        if not Confirm.ask(f"Do you want to delete: [yellow]{task.id}-[/yellow] [bold]{task.title}[/bold]?"):
            console.print("[bold red] Deletion Cancelled [/bold red]")
            return False
        
    session.delete(task)
    session.commit()
    console.print(task, f"\n[green]Task [bold]{task.id}[/bold] deleted successfully ✔[/green]")
    return True
    

def update_task(session: Session, id: int, title: str = None, description: str = None, completed: bool = None, ) -> Task:
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
    return task

def complete_task(session: Session, id: int) -> bool:
    task = update_task(session, id,  completed=True)
    if not task:
        return False
    
    console.print(task, f"\n[green]Task [yellow bold]{id}[/yellow bold] marked as completed successfully ✔[/green]")
    return True

def list_tasks(session: Session, order_by: str = "id", reveresed_flag: bool = False) -> None:
    tasks = get_all_tasks(session, order_by, reveresed_flag)

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


def interactive_edit_task(session: Session, id: int) -> bool:
    CHOICES_TO_EDIT = ['title', 'description', 'complete', 'incomplete']
    task = get_task_by_id(session, id)

    if not task: 
        return False
    
    console.print(task)
    while True: 
        field_to_edit = Prompt.ask("\nSelect the value to edit", choices=CHOICES_TO_EDIT, case_sensitive=False)
    
 
        match field_to_edit:
            case 'title':
                task = update_task(session, id, title=Prompt.ask(f"Enter the new {field_to_edit}"))
            case 'description':
                task = update_task(session, id, description=Prompt.ask(f"\nEnter the new {field_to_edit}"))
            case 'complete':
                task = update_task(session, id, completed=True)
            case 'incomplete':
                task = update_task(session, id, completed=False)
            case _:
                console.print(f"[bold red]Error:[/bold red] [red]Command not recognized ×[/red]")
                return False
        
        console.print('\n', task, f"\n[green]Task [yellow bold]{id}[/yellow bold] editted successfully ✔[/green]\n")

        if not Confirm.ask("Would you like to do another change?"):
            break

    return True

def edit_task(
        session: Session, 
        id: int, 
        title: str = None, 
        description: str = None, 
        completed: bool = None, 
        incomplete: bool = None
        ) -> bool: 
    
    if any([completed, incomplete]):
        completed = True if completed else False
    else:
        completed = None
    
    task = update_task(session, id, title, description, completed)

    if not task:
        return False
    
    console.print(task, f"\n[green]Task [yellow bold]{id}[/yellow bold] editted successfully ✔[/green]\n")
    return True
