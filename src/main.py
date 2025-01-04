from parser import setup_pareser
from task import create_task, delete_task, complete_task, list_tasks, interactive_edit_task, edit_task
from database import Database
from logger import setup_logger, get_logger
from logging import Logger

def main():
    """Entry point for cli-todolist."""    
    
    Database.run_migrations()
    parser = setup_pareser()
    args = parser.parse_args()
    
    if args.debug:
        setup_logger(console_level="DEBUG"),
    else:
        setup_logger()
        
    logger:Logger = get_logger()
    logger.debug(f"Parser Arguments: {args.__dict__}")

    with Database.get_session() as session:
        try:
            match args.command:
                case "create":
                    create_task(session, args.title, args.description)
                case "delete":
                    delete_task(session, args.id, args.interactive)         
                case "complete":
                    complete_task(session, args.id)
                case "list":
                    list_tasks(session,args.sort, args.reversed)
                case "edit":
                    if not any([args.title, args.description, args.completed, args.incomplete]):
                        interactive_edit_task(session, args.id)
                    else:
                        edit_task(session, args.id, args.title, args.description, args.completed, args.incomplete)
                case _: 
                    parser.error("Unrecognized command")
        except KeyboardInterrupt:
            logger.exception("User Excited the Program with KeyboardInterrumpt")
            parser.exit(1)
        except ValueError as e:
            logger.exception(f"ValueError: {e}")
            parser.exit(2)
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            parser.exit(2)

if __name__ == "__main__":
    main()
