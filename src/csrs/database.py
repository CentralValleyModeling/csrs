import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .logger import logger
from .models import Base

DATABASE_NAME = os.environ.get("database-name", "./database/csrs.db")
EPOCH = datetime(1900, 1, 1)
logger.info(f"{DATABASE_NAME=}")


def get_db_dir() -> Path:
    loc = os.environ.get("database-dir", None)
    if loc:
        loc = Path(loc).resolve()
    else:
        loc = Path("./database").resolve()
    if loc.name == "src":
        loc = loc.parent
    if not loc.exists():
        loc.mkdir()
    logger.debug(f"database directory={loc}")
    return loc


def get_database_url(name) -> str:
    url = f"sqlite:///{get_db_dir()}/{name}"
    logger.debug(f"database url={url}")
    return url


def make_engine(database_name) -> Engine:
    logger.debug(f"{database_name=}")
    logger.debug("creating database engine")
    url = get_database_url(database_name)
    return create_engine(url)


def get_session(database_name) -> Session:
    logger.debug("creating database session")
    engine = make_engine(database_name)
    maker = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    # Create database tables
    Base.metadata.create_all(bind=engine)

    return maker()


# Dependency to get a database session
def get_db():
    logger.debug("getting database connection")
    try:
        db = get_session(DATABASE_NAME)
        yield db
    finally:
        db.close()
        logger.debug("closed database")
