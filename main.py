import argparse
from task import Task, console

def main():
    parser = argparse.ArgumentParser(
        prog="Todo", description="A simple Todo list in the CLI"
    )

    # Main command subparser
    command_subparser = parser.add_subparsers(title="Commands", dest="command", description="Available Commands", required=True, metavar="")

    # Create Task Command
    create_parser = command_subparser.add_parser("create", help="Create a new Task")
    create_parser.add_argument("title", type=str, help="Title of the task")
    create_parser.add_argument("-d", "--description", type=str, help="Description of the task")

    # Delete Task Command
    delete_parser = command_subparser.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the Task to be deleted")

    # Mark a Task as Completed Command
    complete_parser = command_subparser.add_parser("complete", help="Mark the Task as Completed")
    complete_parser.add_argument("id", type=int, help="Id of the Task to mark as completed")

    # List all Tasks command
    list_parser = command_subparser.add_parser("list", help="List all current Tasks")

    # Store arguments in a Variable
    args = parser.parse_args()

    # * Test Tasks
    # TODO: Delete this once we have persistent data
    Task.create("Buy Groceries", "Buy Milk, Bread, and Eggs")
    Task.create("Workout", "Go for a 30-minute run")
    Task.create("Read", "Read the book 'Atomic Habits'")
    Task.complete(1)

    match args.command:
        case "create":
            task = Task.create(args.title, args.description)
            print("New Task Created\n",)
            task.show_details()

        case "delete":
            task: Task | bool = Task.delete(args.id)

            if task:
                task.show_details("Deleted Successfully 🗑️")
            else:
                console.print(f"[bold red]Delete Error: Task with id {args.id} does not exist[/bold red]")
                Task.list_all()
                parser.exit(status=2)

        case "complete":
            task: Task | bool = Task.complete(args.id)
            if task:
                task.show_details("Marked as Completed ✔")
            else:
                console.print(f"[bold red]Complete Error: Task with id {args.id} does not exist[/bold red]")
                Task.list_all()
                parser.exit(status=2)

        case "list":
            Task.list_all()


if __name__ == "__main__":
    main()