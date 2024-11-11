import argparse
from task import console, create_task, delete_task, complete_task, list_tasks
from models import Base
from database import engine

def main():
    Base.metadata.create_all(bind=engine)

    parser = argparse.ArgumentParser(
        prog="Todo", description="A simple Todo list in the CLI"
    )

    # Main command subparser
    command_subparser = parser.add_subparsers(title="General Commands", dest="command", description="Available Commands", required=True)

    # Create Task Command
    create_parser = command_subparser.add_parser("create", help="Create a new Task")
    create_parser.add_argument("title", type=str, help="Title of the task")
    create_parser.add_argument("-d", "--description", type=str, help="Description of the task")

    # Delete Task Command
    delete_parser = command_subparser.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the Task to be deleted")
    delete_parser.add_argument("-i", "--interactive", action='store_true', help="Ask for confirmation before deleting the task", default=False)
    # Mark a Task as Completed Command
    complete_parser = command_subparser.add_parser("complete", help="Mark the Task as Completed")
    complete_parser.add_argument("id", type=int, help="Id of the Task to mark as completed")

    # List all Tasks command
    list_parser = command_subparser.add_parser("list", help="List all current Tasks")

    # Store arguments in a Variable
    args = parser.parse_args()
    print()
    
    match args.command:
        case "create":
            create_task(args.title, args.description)
        case "delete":
            delete_task(args.id, args.interactive)
        case "complete":
            complete_task(args.id)
        case "list":
            list_tasks()


if __name__ == "__main__":
    main()
