import argparse

def setup_pareser():
    parser = argparse.ArgumentParser(
        prog="Todo", description="A simple Todo list in the CLI"
    )

    parser.add_argument("--debug", action="store_true", help="Enable Debug Messages")
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
    list_parser.add_argument("-s", "--sort", choices=["id", "title", "completed"], default="id", help="Sort the Task Table. Default: id")
    list_parser.add_argument("-r", "--reversed", action="store_true", help="Reverse the Task Table")

    # Edit Task command
    edit_parser = command_subparser.add_parser('edit', help="Edit the selected Task (Interactive edit by default if no argument is provided)")
    edit_parser.add_argument('id', type=int, help="Id of the Task to edit")

    #Opionals Arguments to Edit the Task directlu
    edit_parser.add_argument("-t", "--title", help="New title value")
    edit_parser.add_argument("-d", "--description", help="New description value")

    # Task completion arguments, MUTUAL EXCLUSIVE
    task_completion = edit_parser.add_mutually_exclusive_group()
    task_completion.add_argument("-c", "--completed", help = "Mark the Task as completed", action="store_true")
    task_completion.add_argument("-i", "--incomplete", help="Mark the Task as incomplete", action="store_true")

    return parser