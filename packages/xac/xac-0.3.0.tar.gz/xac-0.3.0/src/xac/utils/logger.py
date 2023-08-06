import logging
import sys
from logging import FileHandler
from pathlib import Path

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)7s — %(levelname)5s [%(filename)s:%(lineno)s"
    " - %(funcName)20s() ] — %(message)s"
)
LOG_FILE = str(Path.home() / "xac.log")

log_level_dict = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "error": logging.ERROR,
    "warn": logging.WARN,
}


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, log_level: str, file_only=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level_dict.get(log_level, logging.ERROR))
    if not file_only:
        logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
