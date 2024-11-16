from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm
from sqlalchemy.orm import Session
from models import Task
from logger import get_logger

console = Console()
logger = get_logger()

def get_task_by_id(session: Session, id: int) -> Task | None:
    logger.debug(f"Fetching Task with {id=}")
    task = session.query(Task).filter(Task.id == id).first()

    if not task: 
        console.print(f"[bold red]Error:[/bold red] [red]Task with id [yellow bold]{id}[/yellow bold] not found ×[/red]")
        logger.warning(f"Task with {id=} not found")
        return
    
    logger.debug(f"Retrieved Task with {id=} found: {task}")
    return task

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

def get_all_tasks(session: Session, order_by: str = 'id', reveresed_flag: bool = False) -> list[Task]:
    logger.debug(f"Fetching all tasks ordered by {order_by}, reversed: {reveresed_flag}.")
    tasks = session.query(Task).order_by(getattr(Task,order_by)).all()
    logger.debug(f"Retrieved {len(tasks)} tasks.")
    return tasks if not reveresed_flag else list(reversed(tasks))


def create_task(session: Session, title: str, description: str) -> bool:
    logger.debug(f"Creating Task with {title=}, {description=}")
    task = Task(title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    logger.debug(f"Task created: {task}")
    console.print(task, f"\n[green]Task [bold]{task.id}[/bold] created successfully ✔[/green]")
    return True

def delete_task(session: Session, id: int, interactive: bool = False) -> bool:
    logger.debug(f"Deleting Task with {id=}")
    task = get_task_by_id(session, id)
    if not task:
        logger.warning(f"Attempted to delete non-existent task with {id=}.")
        return False
    
    if interactive:
        if not Confirm.ask(f"Do you want to delete: [yellow]{task.id}-[/yellow] [bold]{task.title}[/bold]?"):
            console.print("[bold red] Deletion Cancelled [/bold red]")
            logger.info(f"Deletion of task {id} cancelled by user.")
            return False
        
    session.delete(task)
    session.commit()
    console.print(task, f"\n[green]Task [bold]{task.id}[/bold] deleted successfully ✔[/green]")
    logger.debug(f"Deleted Task with {id=}: {task}")
    return True
    

def update_task(session: Session, id: int, title: str = None, description: str = None, completed: bool = None, ) -> Task | None:
    task = get_task_by_id(session, id)
    if not task:
        logger.warning(f"Attempted to update non-existent task with {id=}.")
        return

    logger.debug(f"Updating Task {task}: {title=}, {description=}, {completed=}")
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
        logger.warning(f"Attempted to mark non-existent task with {id=} as completed.")
        return False
    
    console.print(task, f"\n[green]Task [yellow bold]{id}[/yellow bold] marked as completed successfully ✔[/green]")
    logger.debug(f"Marked Task with {id=} as completed")
    return True

def list_tasks(session: Session, order_by: str = "id", reveresed_flag: bool = False) -> None:
    tasks = get_all_tasks(session, order_by, reveresed_flag)
    logger.debug("Listing tasks.")

    if not tasks:
        logger.info("No tasks available to list.")
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
        logger.warning(f"Attempted to interactive edit non-existent task with {id=}.")
        return False
    
    logger.info(f"Starting interactive edit for task {id}.")
    console.print(task)

    while True: 
        field_to_edit = Prompt.ask("\nSelect the value to edit", choices=CHOICES_TO_EDIT)
        
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
        
        logger.info(f"Task {id} edited: {field_to_edit} updated.")
        console.print('\n', task, f"\n[green]Task [yellow bold]{id}[/yellow bold] editted successfully ✔[/green]\n")

        if not Confirm.ask("Would you like to do another change?"):
            break

    return True
