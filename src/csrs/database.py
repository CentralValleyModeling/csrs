import logging
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import CreateTable

from .config import DatabaseConfig
from .models import Base

logger = logging.getLogger(__name__)
db_cfg = DatabaseConfig()


def create_recipe_file(
    engine: Engine,
    dst: Path | str | None = None,
):
    if dst is None:
        dst = db_cfg.source.with_suffix(".recipe.sql")
    dst = Path(dst).resolve()
    logger.info(f"creating database recipe file: {dst}")
    try:
        with open(dst, "w") as DST:
            for table in Base.metadata.tables.values():
                sql = str(CreateTable(table).compile(engine))
                DST.write(sql.strip() + ";\n\n")
    except PermissionError as e:
        logger.error(
            f"recipe file ({dst}) couldn't be created because of {e.__class__.__name__}"
        )


def make_engine() -> Engine:
    logger.info("creating database engine")
    return create_engine(
        url=db_cfg.url,
        echo=db_cfg.echo,
    )


def init_db(engine: Engine) -> None:
    logger.info("initializing database")
    Base.metadata.create_all(bind=engine)


def make_session(engine: Engine) -> Session:
    logger.debug("creating a new session")
    maker = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    return maker()


# Dependency to get a database session
def get_db():
    db = make_session(ENGINE)
    try:
        yield db
    finally:
        db.close()
        logger.debug("closed database")


ENGINE = make_engine()
create_recipe_file(engine=ENGINE)
if not db_cfg.source.exists():
    logger.warning("creating empty database because it wasn't found")
    init_db(ENGINE)
