import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from uvicorn.logging import ColourizedFormatter

from .config import LogConfig


def get_dir() -> Path:
    here = Path(".").resolve()

    return here


def config_uvicorn_logging(config: LogConfig):
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "uvicorn.asgi"):
        logger = logging.getLogger(logger_name)
        console_formatter = ColourizedFormatter(config.fmt, datefmt=config.datefmt)
        for h in logger.handlers:
            h.setFormatter(console_formatter)


def get_logger() -> logging.Logger:
    log_cfg = LogConfig()
    logger = logging.getLogger("csrs")
    logger.setLevel(log_cfg.level)
    # make formatter for these logging handlers
    formatter = ColourizedFormatter(fmt=log_cfg.fmt, datefmt=log_cfg.datefmt)
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
    config_uvicorn_logging(log_cfg)
    return logger


logger = get_logger()
