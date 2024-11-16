from parser import setup_pareser
from task import create_task, delete_task, complete_task, list_tasks, interactive_edit_task, edit_task
from database import Database
from logger import setup_logger, get_logger

def main():
    """Entry point for cli-todolist."""    
    
    Database.run_migrations()

    parser = setup_pareser()

    # Store arguments in a Variable
    args = parser.parse_args()
    print()
    if args.debug:
        setup_logger(console_level="DEBUG"),
    else:
        setup_logger()
        
    logger = get_logger()
    logger.debug(f"Parser Arguments: {args.__dict__}")

    with Database.get_session() as session:
        try:
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
                    list_tasks(session,args.sort, args.reversed)
                case "edit":
                    if not any([args.title, args.description, args.completed, args.incomplete]):
                        if not interactive_edit_task(session, args.id):
                            parser.exit(2)
                    else:
                        if not edit_task(session, args.id, args.title, args.description, args.completed, args.incomplete):
                            parser.exit(2)
                case _: 
                    parser.error("Unrecognized command")
        except KeyboardInterrupt:
            logger.exception("User Excited the Program with KeyboardInterrumpt")

if __name__ == "__main__":
    main()
