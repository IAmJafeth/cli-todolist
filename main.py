import argparse
from task import console, create_task, delete_task, complete_task, list_tasks, interactive_edit
from models import Base
from database import engine, get_session

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
    delete_parser.add_argument("id", type=int, help="Id of the Task to delete")
    delete_parser.add_argument("-i", "--interactive", action='store_true', help="Ask for confirmation before deleting the task", default=False)
    # Mark a Task as Completed Command
    complete_parser = command_subparser.add_parser("complete", help="Mark the Task as Completed")
    complete_parser.add_argument("id", type=int, help="Id of the Task to mark as completed")

    # List all Tasks command
    list_parser = command_subparser.add_parser("list", help="List all current Tasks")

    # Edit Task command
    edit_parser = command_subparser.add_parser('edit', help="Edit the selected Task")
    edit_parser.add_argument('id', type=int, help="Id of the Task to edit")

    # Store arguments in a Variable
    args = parser.parse_args()
    print()
    
    with get_session() as session:

        match args.command:
            case "create":
                if not create_task(session, args.title, args.description):
                    parser.exit(2)
            case "delete":
                if not delete_task(session, args.id, args.interactive):
                    parser.exit(2)            
            case "complete":
                if not complete_task(session, args.id):
                    parser.exit(2)
            case "list":
                list_tasks(session)
            case "edit":
                if not interactive_edit(session, args.id):
                    parser.exit(2)
            case _: 
                parser.error("Unrecognized command")

if __name__ == "__main__":
    main()
