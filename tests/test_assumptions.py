import os
import sys

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append("./src")

from calsim_scenario_server.client import CalSimScenarioClient
from calsim_scenario_server.database import get_db
from calsim_scenario_server.main import app
from calsim_scenario_server.models import Base
from calsim_scenario_server.schemas import Assumption, Scenario

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

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
test_client = TestClient(app)


def test_testing_on_local():
    from pathlib import Path

    import calsim_scenario_server

    here = Path(__file__).parent
    mod_path = Path(calsim_scenario_server.__file__).parent

    rel = mod_path.relative_to(here.parent)
    assert str(rel) == "src\\calsim_scenario_server"


def test_put_assumption():
    a_in = Assumption(
        name="example",
        detail="this is an example assumption",
        kind="tucp",
    )
    print(a_in.model_dump_json(exclude="id"))
    response = test_client.put("/assumptions/tucp", json=a_in.model_dump(exclude="id"))
    response.raise_for_status()
    a_out = Assumption.model_validate(response.json())
    assert a_out.id == 1


def test_get_assumption():
    client = CalSimScenarioClient(base_url="http://localhost")
    client.client = test_client
    values = client.get_assumption(kind="tucp")
    assert len(values) == 1
    assert values[0].id == 1


def test_put_scenario():
    assumpt_base = {"name": "add_sceanrio_example", "detail": "foo bar baz"}
    assumptions = {c: {"kind": c, **assumpt_base} for c in Scenario.model_fields}
    response = test_client.get("/assumptions")
    response.raise_for_status()
    values = response.json()
    names = dict()
    for name in values:
        response = test_client.put(f"/assumptions/{name}", json=assumptions[name])
        response.raise_for_status()
        assumption = response.json()
        names[name] = assumption["name"]
    print(names)
    scenario_data = dict(name="test_add_scenario", **names)
    response = test_client.put("/scenarios", json=scenario_data)
    response.raise_for_status()
    value = response.json()
    assert value["name"] == "test_add_scenario"


def test_get_scenario():
    response = test_client.get("/scenarios")
    response.raise_for_status()
    values = response.json()
    assert len(values) == 1
    assert values[0]["name"] == "test_add_scenario"
