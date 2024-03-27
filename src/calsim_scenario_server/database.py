import os
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

DATABASE_NAME = os.environ.get("DATABASE_NAME", "example")


def get_db_dir() -> Path:
    here = Path(".").resolve()
    if here.name == "src":
        here = here.parent
    return here


def get_database_url(name: str = "example") -> str:
    return f"sqlite:///{get_db_dir()}/{name}.sqlite"


def make_engine(database_name: str = "example") -> Engine:
    url = get_database_url(database_name)
    return create_engine(url)


def get_session(database_name: str = "example") -> sessionmaker:
    engine = make_engine(database_name)
    maker = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    # Create database tables
    Base.metadata.create_all(bind=engine)

    return maker


# Dependency to get a database session
def get_db():
    db = get_session(DATABASE_NAME)
    try:
        yield db
    finally:
        db.close()
