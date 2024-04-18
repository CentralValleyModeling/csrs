from os import remove
from pathlib import Path
from time import sleep

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from calsim_scenario_server import app, clients
from calsim_scenario_server.database import get_db
from calsim_scenario_server.models import Base


@pytest.fixture(scope="session", autouse=True)
def client_local():
    db = Path(__file__).parent / "assets/test_local_client.sqlite"
    client = clients.LocalClient(db_path=db)
    yield client
    client.close()
    # Delete the testing db
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


@pytest.fixture(scope="session", autouse=True)
def client_server():
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
