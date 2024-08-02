import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import CreateTable

from .logger import logger
from .models import Base

ENVIRONMENT_KEY = "DATABASE_CSRS"
DATABASE = Path(os.environ.get(ENVIRONMENT_KEY, "./database/csrs.db")).resolve()
EPOCH = datetime(1900, 1, 1)
ALLOW_DOWNLOAD = True


def get_database_url(db: str = DATABASE, db_type="sqlite") -> str:
    if db_type == "sqlite":
        url = f"sqlite:///{db}"
    else:
        raise NotImplementedError(f"{db_type=} not supported")
    logger.debug(f"{url=}")
    return url


def make_engine(db, echo: bool = False) -> Engine:
    logger.debug(f"{db=}")
    logger.debug("creating database engine")
    url = get_database_url(db)
    engine = create_engine(url, echo=echo)
    create_recipe_file(engine=engine)
    return engine


def make_session(engine) -> Session:
    logger.debug("creating database session")
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
        yield SESSION
    finally:
        SESSION.close()
        logger.debug("closed database")


def create_recipe_file(engine: Engine, dst: Path | str | None = None):
    if dst is None:
        dst = Path(__file__).parent / "database_recipe.sql"
    dst = Path(dst).resolve()
    logger.info(f"creating database recipe file: {dst}")
    with open(dst, "w") as DST:
        for table in Base.metadata.tables.values():
            sql = str(CreateTable(table).compile(engine))
            DST.write(sql.strip() + ";\n\n")


ENGINE = make_engine(DATABASE)
SESSION = make_session(ENGINE)
