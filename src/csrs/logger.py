import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def get_dir() -> Path:
    here = Path(".").resolve()
    if here.name == "src":
        here = here.parent

    return here


def get_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    level = int(os.environ.get("log-level", logging.INFO))
    logger.setLevel(level)
    # make formatter for these logging handlers
    formatter = logging.Formatter(
        "%(asctime)s "
        + "[%(levelname)s] "
        + "%(funcName)s: "
        + "%(name)s: "
        + "%(message)s"
    )
    # Set up handler for sending logs to file
    file_handler_kwargs = dict(
        filename=get_dir() / "debug.log",
        when="d",
        backupCount=8,  # One more day than a week
    )
    file_handler = TimedRotatingFileHandler(**file_handler_kwargs)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Set up handler to send logs to stdout
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


logger = get_logger()
