import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .logger import logger
from .models import Base

DATABASE = Path(os.environ.get("database-name", "./database/csrs.db")).resolve()
EPOCH = datetime(1900, 1, 1)


def get_database_url(db, db_type="sqlite") -> str:
    if db_type == "sqlite":
        url = f"sqlite:///{db}"
    else:
        raise NotImplementedError(f"{db_type=} not supported")
    logger.debug(f"{url=}")
    return url


def make_engine(db) -> Engine:
    logger.debug(f"{db=}")
    logger.debug("creating database engine")
    url = get_database_url(db)
    return create_engine(url)


def get_session(db) -> Session:
    logger.debug("creating database session")
    engine = make_engine(db)
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
        db = get_session(DATABASE)
        yield db
    finally:
        db.close()
        logger.debug("closed database")
