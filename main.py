import argparse


class Task:

    index: int = 0

    def __init__(
        self,
        title: str,
        completed = True
    ) -> None:
        self.title: str = title
        self.index = Task.index
        Task.index += 1


parser = argparse.ArgumentParser(
    prog="cli-todo", description="A simple Todo list in the CLI"
)

command_subparser = parser.add_subparsers(title="Commands", dest="command", description="Available Commands", required=True, metavar="")

create_parser = command_subparser.add_parser("create", help="Create a new Task")
create_parser.add_argument("name", type=str, help="Name of the task")
create_parser.add_argument("-d", "--description", type=str, help="Description of the task")

delete_parser = command_subparser.add_parser("delete", help="Delete a task")
delete_parser.add_argument("id", type=int, help="ID of the Task to be deleted")

complete_parser = command_subparser.add_parser("complete", help="Mark the Task as Completed")
complete_parser.add_argument("id", type=int, help="Id of the Task to mark as completed")

list_parser = command_subparser.add_parser("list", help="List all current Tasks")

parser.parse_args()