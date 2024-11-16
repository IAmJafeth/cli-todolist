import logging
from rich.logging import RichHandler
import os

LOGGER_NAME = "todolist"
CONSOLE_LOG_LEVEL = "CRITICAL"
FILE_LOG_LEVEL = "DEBUG"

if not os.path.exists("../data"):
    os.makedirs("../data")

def setup_logger(logger_name: str = LOGGER_NAME, console_level: str = CONSOLE_LOG_LEVEL, file_level: str = FILE_LOG_LEVEL) -> None:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(f"../data/{f"{logger_name}.log"}")
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = RichHandler(markup=True, rich_tracebacks=True, tracebacks_show_locals=True)
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def get_logger(logger_name: str = LOGGER_NAME) -> logging.Logger:
    return logging.getLogger(logger_name)
