import logging
from datetime import datetime
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from . import __version__


def log_config_values(config: BaseSettings):
    logger = logging.getLogger("csrs.init")
    logger.setLevel(logging.DEBUG)
    for name in config.model_fields:
        if name.startswith("_"):
            pass
        v = getattr(config, name)
        logger.debug(f"{config.__class__.__name__}.{name} = {repr(v)}")


class LoggedSettings(BaseSettings):
    def model_post_init(self, _):
        log_config_values(self)


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
    db: Path = Path("csrs.db").resolve()
    epoch: datetime = datetime(1900, 1, 1)
    allow_download: bool = True
    allow_editing_via_forms: bool = False

    model_config = SettingsConfigDict(env_file=".database")


class LogConfig(LoggedSettings):
    level: int | str = "INFO"
    fmt: str = "%(levelprefix)s %(asctime)s [%(funcName)s] %(message)s "
    datefmt: str = "%Y-%m-%d %H:%M:%S"
    model_config = SettingsConfigDict(env_file=".logging")
