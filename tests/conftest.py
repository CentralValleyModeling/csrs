import logging
from os import remove
from pathlib import Path
from shutil import copy2
from time import sleep

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.schema import CreateTable

from csrs import clients
from csrs.database import get_db, make_session
from csrs.main import app
from csrs.models import Base


@pytest.fixture(scope="session")
def empty_database() -> Session:
    engine = create_engine("sqlite:///:memory:", echo=True)
    for table in Base.metadata.tables.values():
        sql = str(CreateTable(table).compile(engine))
        with open("sql.txt", "a+") as S:
            S.write(sql)
    return make_session(engine)


@pytest.fixture(scope="session")
def assets_dir() -> Path:
    return Path(__file__).parent / "assets"


@pytest.fixture(scope="function", autouse=True)
def client_local(assets_dir):
    db = assets_dir / "testing_local_client.db"
    client = clients.LocalClient(db_path=db)
    yield client
    client.close()
    # Delete the testing db
    # TODO: 2024-07-31 Do the deletion more elegantly
    attempts = 0
    error = None
    while db.exists() and (attempts < 10):
        try:
            remove(db)
        except PermissionError as e:
            error = e
            attempts += 1
            sleep(1)
    if db.exists() and error:
        raise error


@pytest.fixture(scope="function", autouse=True)
def client_remote():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def get_testing_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_testing_db
    client = clients.RemoteClient(base_url="http://localhost")
    client.actor = TestClient(app)  # TODO: move this to a method

    yield client


@pytest.fixture(scope="session")
def database(assets_dir: Path) -> Session:
    starting_db = assets_dir / "_testing.db"
    active_db = starting_db.with_name("testing_dirty.db")
    if active_db.exists():  # remove "dirty" databases from old testing run
        remove(active_db)
    if starting_db.exists():  # active will be made automatically if not there
        copy2(starting_db, active_db)
    database_url = "sqlite:///" + str(active_db)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    return make_session(engine)


@pytest.fixture(scope="session")
def dss(assets_dir):
    return assets_dir / "testing.dss"


@pytest.fixture(scope="module")
def kwargs_assumption():
    return dict(
        name="testing-create-assumption",
        kind="testing",
        detail="testing assumption",
    )


@pytest.fixture(scope="module")
def kwargs_assumption_duplicate():
    return dict(
        name="testing-create-assumption-duplicate",
        kind="testing",
        detail="testing assumption, testing error on duplicate",
    )


@pytest.fixture(scope="module")
def kwargs_scenario():
    return dict(
        name="testing-create-scenario",
        assumptions=dict(
            testing="testing-preexisting-assumption",
        ),
        detail="testing scenario creation",
    )


@pytest.fixture(scope="module")
def kwargs_run():
    return dict(
        scenario="testing-create-run-scenario",
        version="0.2",
        contact="user@email.com",
        code_version="0.1",
        detail="testing-create-run",
    )


@pytest.fixture(scope="module")
def kwargs_path():
    return dict(
        name="testing-create-timeseries",
        path="/.*/TESTING_CREATE/TESTING/.*/.*/.*/",
        category="testing",
        period_type="PER-AVER",
        interval="1MON",
        units="NONE",
        detail="A testing timeseries meant to be created during a test",
    )
