import argparse
from task import Task

parser = argparse.ArgumentParser(
    prog="Todo", description="A simple Todo list in the CLI"
)

command_subparser = parser.add_subparsers(title="Commands", dest="command", description="Available Commands", required=True, metavar="")

create_parser = command_subparser.add_parser("create", help="Create a new Task")
create_parser.add_argument("title", type=str, help="Title of the task")
create_parser.add_argument("-d", "--description", type=str, help="Description of the task")

delete_parser = command_subparser.add_parser("delete", help="Delete a task")
delete_parser.add_argument("id", type=int, help="ID of the Task to be deleted")

complete_parser = command_subparser.add_parser("complete", help="Mark the Task as Completed")
complete_parser.add_argument("id", type=int, help="Id of the Task to mark as completed")

list_parser = command_subparser.add_parser("list", help="List all current Tasks")

args = parser.parse_args()

command: str = args.command

Task.create("Task1", "A small description")
Task.create("Task2", None)

match command:
    case "create":
        task = Task.create(args.title, args.description)
        print("New Task Created\n", task)

    case "delete":
        task: Task | bool = Task.delete(args.id)

        if task:
            print(f"Task {args.id} Deleted Succesfully\n\n", task)
        else:
            parser.exit(message=f"Error: Task with id: \"{args.id}\" does not exist", status=2)

    case "complete":
        task: Task | bool = Task.complete(args.id)
        if task:
            print(f"Task {args.id} marked as compelted\n\n",task)
        else:
            parser.exit(message=f"Task with id: \"{args.id}\" does not exist", status=2)

    case "list":
        Task.list()