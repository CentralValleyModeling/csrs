import logging
from pathlib import Path
from shutil import copy2
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from csrs import clients
from csrs.database import get_db, make_session
from csrs.main import app
from csrs.models import Base


@pytest.fixture(scope="session")
def assets_dir() -> Path:
    return Path(__file__).parent / "assets"


@pytest.fixture(scope="session")
def dss(assets_dir: Path) -> Generator[Path, None, None]:
    starting = assets_dir / "_testing.dss"
    active = assets_dir / "testing_used.dss"
    if active.exists():
        active.unlink()
    if starting.exists():
        copy2(starting, active)
    yield active
    active.unlink()
    for f in active.parent.iterdir():
        if (f.stem == active.stem) and (f.suffix.startswith(".ds")):
            try:
                f.unlink()
            except PermissionError:
                logging.warning(f"couldn't remove testing asset {f}")


@pytest.fixture(scope="session")
def database_file(assets_dir: Path) -> Generator[Path, None, None]:
    starting = assets_dir / "_testing.db"
    active = starting.with_name("testing_used.db")
    if active.exists():
        active.unlink()
    if starting.exists():  # active will be made automatically if not there
        copy2(starting, active)
    yield active
    try:
        active.unlink()
    except PermissionError:
        logging.warning(f"couldn't remove testing asset {active}")


@pytest.fixture(scope="session")
def database_url(database_file: Path) -> str:
    return "sqlite:///" + str(database_file)


@pytest.fixture(scope="session")
def database(database_url: Path) -> Generator[Session, None, None]:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    with make_session(engine) as session:
        yield session
    session.close()
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def client_local(database_file: Path):
    client = clients.LocalClient(db_path=database_file)
    yield client
    client.close()


@pytest.fixture(scope="session", autouse=True)
def client_remote(database_url: str):
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
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
    client.actor.close()


@pytest.fixture(scope="module")
def kwargs_assumption():
    return dict(
        name="testing-assumption-new",
        kind="testing",
        detail="testing assumption",
    )


@pytest.fixture(scope="module")
def kwargs_assumption_duplicate():
    return dict(
        name="testing-assumption-new-duplicate",
        kind="testing",
        detail="testing assumption, testing error on duplicate",
    )


@pytest.fixture(scope="module")
def kwargs_scenario():
    return dict(
        name="testing-scenario-new",
        assumptions=dict(
            testing="testing-assumption-existing",
        ),
    )


@pytest.fixture(scope="module")
def kwargs_run():
    return dict(
        scenario="testing-scenario-existing",
        version="0.2",
        contact="test@testing.gov",
        code_version="0.1",
        detail="testing-create-run",
    )


@pytest.fixture(scope="module")
def kwargs_path():
    return dict(
        name="testing-path-new",
        path="/.*/TESTING_CREATE/TESTING/.*/.*/.*/",
        category="testing",
        period_type="PER-AVER",
        interval="1MON",
        units="NONE",
        detail="A testing path meant to be created during a test",
    )


@pytest.fixture(scope="function")
def kwargs_all_unique():
    uuid = id(object())
    return dict(
        assumption=dict(
            name=f"testing-assumption-new-{uuid}",
            kind="testing",
            detail=f"testing assumption, with unique id {uuid}",
        ),
        scenario=dict(
            name=f"testing-scenario-new-{uuid}",
            assumptions=dict(
                testing="testing-assumption-existing",
            ),
        ),
        run=dict(
            scenario="testing-scenario-existing",
            version=f"0.0.{uuid}",
            contact="test@testing.gov",
            code_version="0.1",
            detail=f"testing-create-run-{uuid}",
        ),
        path=dict(
            name=f"testing-path-new-{uuid}",
            path=f"/CSRS/TESTING_NEW_{uuid}/TESTING/.*/1MON/2024/",
            category="testing",
            period_type="PER-AVER",
            interval="1MON",
            units="NONE",
            detail="A testing path meant to be created during a test,"
            + f" with a unique id: {uuid}",
        ),
        timeseries=dict(
            scenario="testing-scenario-existing",
            version=f"0.0.{uuid}",
            path="/CSRS/TESTING_EXISTING_CLIENT/TESTING/.*/1MON/2024/",
            values=(1.0, 2.0, 3.0),
            dates=("1921-10-30", "1921-11-30", "1921-12-31"),
            period_type="PER-AVER",
            units="NONE",
            interval="1MON",
        ),
    )
