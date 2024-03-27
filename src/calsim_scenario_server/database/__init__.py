from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..models import Base


def get_db_dir() -> Path:
    here = Path(".").resolve()
    if here.name == "src":
        here = here.parent
    return here


DATABASE_URL = f"sqlite:///{get_db_dir()}/example.sqlite"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database tables
Base.metadata.create_all(bind=engine)


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
