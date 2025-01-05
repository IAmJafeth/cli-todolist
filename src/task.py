from typing import Type

from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm
from sqlalchemy.orm import Session
from models import Task
from logger import get_logger
from src.models import Task

console = Console()
logger = get_logger()

def get_task_by_id(session: Session, task_id: int) -> Task:
    """Fetch a task with the given id from the database.

    Args:
        session (Session): The SQLAlchemy Session object.
        task_id (int): The id of the task to fetch.

    Raises:
        ValueError: If the task with the given id is not found

    Returns:
        Task: The Task object
    """

    logger.debug(f"Fetching Task with {task_id=}")
    task: Task | None= session.query(Task).filter(Task.id == task_id).first()

    if not task: 
        console.print(f"[bold red]Error:[/bold red] [red]Task with id [yellow bold]{task_id}[/yellow bold] not found ×[/red]")
        logger.warning(f"Task with {task_id=} not found")
        raise ValueError(f"Task with id {task_id} not found.")
    
    logger.debug(f"Retrieved Task with {task_id=} found: {task}")
    return task

def edit_task(
        session: Session, 
        task_id: int,
        title: str = None, 
        description: str = None, 
        completed: bool = None, 
        incomplete: bool = None
        ) -> None: 
    """Edit a task with the given values.
    
    Args:
        session (Session): The SQLAlchemy Session object.
        task_id (int): The id of the task to edit.
        title (str, optional): The new title for the task. Defaults to None.
        description (str, optional): The new description for the task. Defaults to None.
        completed (bool, optional): Mark the task as completed. Defaults to None.
        incomplete (bool, optional): Mark the task as incomplete. Defaults to None.

    Raises:
        ValueError: If the task with the given id is not found

    Returns:
        None: None
    """
    if any([completed, incomplete]):
        completed = True if completed else False
    else:
        completed = None
    
    task = update_task(session, task_id, title, description, completed)
    
    console.print(task, f"\n[green]Task [yellow bold]{task_id}[/yellow bold] edited successfully ✔[/green]\n")

def get_all_tasks(session: Session, order_by: str = 'id', reversed_flag: bool = False) -> list[Type[Task] | list[None]]:
    """Fetch all tasks from the database.

    Args:
        session (Session): The SQLAlchemy Session object.
        order_by (str, optional): The column to order by. Defaults to 'id'.
        reversed_flag (bool, optional): Whether to reverse the order. Defaults to False.

    Raises:
        Exception: If there is an error fetching tasks

    Returns:
        list[Type[Task] | list[None]]: A list of Task objects
    """

    logger.debug(f"Fetching all tasks ordered by {order_by}, reversed: {reversed_flag}.")
    try:
        tasks = session.query(Task).order_by(getattr(Task,order_by)).all()
    except Exception as e:
        logger.exception(f"Error fetching tasks: {e}")
        console.print(f"[bold red]Error:[/bold red] [red]Error fetching tasks: {e} ×[/red]")
        raise e
    logger.debug(f"Retrieved {len(tasks)} tasks.")
    return tasks if not reversed_flag else list(reversed(tasks))


def create_task(session: Session, title: str, description: str) -> Task:
    """Create a new task with the given title and description.

    Args:
        session (Session): The SQLAlchemy Session object.
        title (str): The title of the task.
        description (str): The description of the task.
    
    Raises:
        Exception: If there is an error creating the task

    Returns:
        None: None
    """

    logger.debug(f"Creating Task with {title=}, {description=}")
    task = Task(title=title, description=description)
    try:
        session.add(task)
        session.commit()
        session.refresh(task)
    except Exception as e:
        logger.exception(f"Error creating task: {e}")
        console.print(f"[bold red]Error:[/bold red] [red]Error creating task: {e} ×[/red]")
        session.rollback()
        raise e

    logger.debug(f"Task created: {task}")
    console.print(task, f"\n[green]Task [bold]{task.id}[/bold] created successfully ✔[/green]")
    return task

def delete_task(session: Session, task_id: int, interactive: bool = False) -> None:
    """Delete a task with the given id.	

    Args:
        session (Session): The SQLAlchemy Session object.
        task_id (int): The id of the task to delete.
        interactive (bool, optional): Whether to ask for confirmation before deleting. Defaults to False.

    Raises:
        ValueError: If the task with the given id is not found
        Exception: If there is an error deleting the task

    Returns:    
        None: None
    """
    logger.debug(f"Deleting Task with {task_id=}")
    task = get_task_by_id(session, task_id)
    
    if interactive:
        if not Confirm.ask(f"Do you want to delete: [yellow]{task.id}-[/yellow] [bold]{task.title}[/bold]?"):
            console.print("[bold red] Deletion Cancelled [/bold red]")
            logger.info(f"Deletion of task {task_id} cancelled by user.")
            return
    
    try:
        session.delete(task)
        session.commit()
    except Exception as e:
        logger.exception(f"Error deleting task: {e}")
        console.print(f"[bold red]Error:[/bold red] [red]Error deleting task: {e} ×[/red]")
        session.rollback()
        raise e
    
    console.print(task, f"\n[green]Task [bold]{task.id}[/bold] deleted successfully ✔[/green]")
    logger.debug(f"Deleted Task with {task_id=}: {task}")
    

def update_task(session: Session, task_id: int, title: str = None, description: str = None, completed: bool = None, ) -> Task :
    """Update a task with the given values.

    Args:
        session (Session): The SQLAlchemy Session object.
        task_id (int): The id of the task to update.
        title (str, optional): The new title for the task. Defaults to None.
        description (str, optional): The new description for the task. Defaults to None.
        completed (bool, optional): Mark the task as completed. Defaults to None.

    Raises:
        ValueError: If the task with the given id is not found

    Returns:
        Task: The updated Task object
    """

    task = get_task_by_id(session, task_id)

    logger.debug(f"Updating Task {task}: {title=}, {description=}, {completed=}")
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed

    try:
        session.commit()
        session.refresh(task)
    except Exception as e:
        logger.exception(f"Error updating task: {e}")
        console.print(f"[bold red]Error:[/bold red] [red]Error updating task: {e} ×[/red]")
        session.rollback()
        raise e

    return task

def complete_task(session: Session, task_id: int) -> Task:
    """Mark a task as completed.

    Args:
        session (Session): The SQLAlchemy Session object.
        task_id (int): The id of the task to mark as completed.

    Raises:
        ValueError: If the task with the given id is not found
        Exception: If there is an error marking the task as completed

    Returns:
        Task: The updated Task object
    """

    task = update_task(session, task_id, completed=True)
    console.print(task, f"\n[green]Task [yellow bold]{task_id}[/yellow bold] marked as completed successfully ✔[/green]")
    logger.debug(f"Marked Task with {task_id=} as completed")

    return task

def list_tasks(session: Session, order_by: str = "id", reversed_flag: bool = False) -> None:
    """List all tasks.

    Args:
        session (Session): The SQLAlchemy Session object.
        order_by (str, optional): The column to order by. Defaults to "id".
        reversed_flag (bool, optional): Whether to reverse the order. Defaults to False.

    Returns:
        None: None
    """

    tasks = get_all_tasks(session, order_by, reversed_flag)
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


def interactive_edit_task(session: Session, task_id: int) -> Task:
    """Start an interactive edit session for a task.

    Args:
        session (Session): The SQLAlchemy Session object.
        task_id (int): The id of the task to edit.

    Exceptions:
        ValueError: If the task with the given id is not found
        Exception: If there is an error updating the task

    Returns:
        Task: The updated Task object
    """
    CHOICES_TO_EDIT = ['title', 'description', 'complete', 'incomplete']
    task = get_task_by_id(session, task_id)
    
    logger.info(f"Starting interactive edit for task {task_id}.")
    console.print(task)

    while True: 
        field_to_edit = Prompt.ask("\nSelect the value to edit", choices=CHOICES_TO_EDIT)
        
        match field_to_edit:
            case 'title':
                task = update_task(session, task_id, title=Prompt.ask(f"Enter the new {field_to_edit}"))
            case 'description':
                task = update_task(session, task_id, description=Prompt.ask(f"\nEnter the new {field_to_edit}"))
            case 'complete':
                task = update_task(session, task_id, completed=True)
            case 'incomplete':
                task = update_task(session, task_id, completed=False)
            case _:
                console.print(f"[bold red]Error:[/bold red] [red]Command not recognized ×[/red]")
                logger.error(f"Invalid command: {field_to_edit}")
                continue
        
        logger.info(f"Task {task_id} edited: {field_to_edit} updated.")
        console.print('\n', task, f"\n[green]Task [yellow bold]{task_id}[/yellow bold] edited successfully ✔[/green]\n")

        if not Confirm.ask("Would you like to do another change?"):
            break
    return task
