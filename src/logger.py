import logging
from rich.logging import RichHandler

LOGER_NAME = "todolist"

def setup_logger(debug: bool = False) -> None:
    LOG_FILE = f"{LOGER_NAME}.log"

    logger = logging.getLogger(LOGER_NAME)
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(f"../{LOG_FILE}")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Console handler
    debug_level = logging.CRITICAL if not debug else logging.DEBUG
    console_handler = RichHandler(markup=True, rich_tracebacks=True, tracebacks_show_locals=True)
    console_handler.setLevel(debug_level)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def get_logger() -> logging.Logger:
    return logging.getLogger(LOGER_NAME)
