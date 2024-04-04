import requests
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from calsim_scenario_server.database import get_db
from calsim_scenario_server.main import app
from calsim_scenario_server.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_add_assumption(base_url: str):
    assumption = {"name": "example", "detail": "this is an example assumption"}
    response = requests.put(base_url + "/assumptions/tucp", json=assumption)
    response.raise_for_status()
    assert response["id"] == 1


def test_get_assumption(base_url: str):
    responses = get_json(base_url + "/assumptions/tucp")
    assert len(responses) == 1
    assert responses[0]["id"] == 1
