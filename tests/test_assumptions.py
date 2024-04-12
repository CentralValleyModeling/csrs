import sys

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append("./src")

from calsim_scenario_server.database import get_db
from calsim_scenario_server.main import app
from calsim_scenario_server.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
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
client = TestClient(app)


def test_add_assumption():
    assumption = {"name": "example", "detail": "this is an example assumption"}
    response = client.put("/assumptions/tucp", json=assumption)
    response.raise_for_status()
    values = response.json()
    assert values["id"] == 1


def test_get_assumption():
    response = client.get("/assumptions/tucp")
    response.raise_for_status()
    values = response.json()
    assert len(values) == 1
    assert values[0]["id"] == 1


def test_put_scenario():
    basic_info = {"name": "add_sceanrio_example", "detail": "foo bar baz"}
    assumptions = {
        "dcp": basic_info,
        "hydrology": basic_info,
        "land_use": dict(additional_metadata={"future_year": 2020}, **basic_info),
        "sea_level_rise": dict(additional_metadata={"centimeters": 0}, **basic_info),
        "sod": basic_info,
        "tucp": basic_info,
        "va": basic_info,
    }
    response = client.get("/assumptions")
    response.raise_for_status()
    values = response.json()
    id_values = dict()
    for name in values:
        response = client.put(f"/assumptions/{name}", json=assumptions[name])
        response.raise_for_status()
        assumption = response.json()
        id_values[name] = {"id": assumption["id"]}
    scenario_data = dict(name="test_add_scenario", assumptions_used=id_values)
    print(scenario_data)
    response = client.put("/scenarios", json=scenario_data)
    response.raise_for_status()
    value = response.json()
    assert value["name"] == "test_add_scenario"


def test_get_scenario():
    response = client.get("/scenarios")
    response.raise_for_status()
    values = response.json()
    assert len(values) == 1
    assert values[0]["name"] == "test_add_scenario"
