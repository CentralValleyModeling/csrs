import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def get_dir() -> Path:
    here = Path(".").resolve()
    if here.name == "src":
        here = here.parent


def get_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(
        get_dir() / "debug.log",
        when="d",
        backupCount=8,  # One more day than a week
    )
    formatter = logging.Formatter(
        "%(asctime)s "
        + "[%(levelname)s] "
        + "%(funcName)s: "
        + "%(name)s: "
        + "%(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = get_logger()
