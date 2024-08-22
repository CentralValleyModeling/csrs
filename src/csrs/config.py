import logging
import logging.handlers
import sys
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from uvicorn.logging import ColourizedFormatter

from . import __version__


class LoggedSettings(BaseSettings):
    def model_post_init(self, _):
        logger = logging.getLogger(__name__)
        for name in self.model_fields:
            if name.startswith("_"):
                pass
            v = getattr(self, name)
            logger.debug(f"{self.__class__.__name__}.{name} = {repr(v)}")


class AppConfig(LoggedSettings):
    title: str = "CalSim Scenario Results Server"
    summary: str = "Interact with CalSim3 results and metadata."
    contact: dict = {
        "name": "California DWR, Central Valley Modeling",
        "url": "https://water.ca.gov/Library/"
        + "Modeling-and-Analysis/Central-Valley-models-and-tools",
    }
    license_info: dict = {
        "name": "MIT",
        "identifier": "MIT",
    }
    version: str = __version__ or "dev"
    docs_url: str = "/docs"
    model_config = SettingsConfigDict(env_file=".app")


class DatabaseConfig(LoggedSettings):
    source: Path = Path("csrs.db").resolve()
    echo: bool = False
    allow_download: bool = True
    allow_editing_via_forms: bool = False
    model_config = SettingsConfigDict(env_file=".database")

    @property
    def url(self) -> str:
        return f"sqlite:///{self.source}"


class LogConfig(LoggedSettings):
    level: int | str = "INFO"
    fmt: str = "%(levelprefix)s %(asctime)s [%(name)s] %(message)s "
    datefmt: str = "%Y-%m-%d %H:%M:%S"
    use_colors: bool = True
    asgi_level: int | str = "INFO"
    model_config = SettingsConfigDict(env_file=".logging")


def get_csrs_logger():
    logger_name = __name__
    while (not logger_name.endswith("csrs")) and (logger_name.count(".")):
        logger_name = logger_name.rsplit(".", 1)[0]
    return logging.getLogger(logger_name)


def configure_logging(
    logger: logging.Logger,
    cfg: LogConfig | None = None,
):
    # Load the configuration file
    if cfg is None:
        cfg = LogConfig()
    # Configure the csrs logger with two handlers, and one format
    logger.setLevel(cfg.level)
    # make formatter for these logging handlers
    csrs_log_formatter = ColourizedFormatter(
        fmt=cfg.fmt,
        datefmt=cfg.datefmt,
        use_colors=cfg.use_colors,
    )
    # Make the two handlers
    # Set up handler for sending logs to file
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=Path(".").resolve() / "debug.log",
        when="d",
        backupCount=8,  # One more day than a week
    )
    file_handler.setFormatter(csrs_log_formatter)
    # Set up handler to send logs to stdout
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(csrs_log_formatter)
    # Add the handlers to the csrs logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    # configure uvicorn to use the same logging format
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "uvicorn.asgi"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.setLevel(cfg.asgi_level)
        for h in uvicorn_logger.handlers:
            h.setFormatter(csrs_log_formatter)

    logger.debug("logging configured to csrs standard")
