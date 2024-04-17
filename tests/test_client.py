from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from calsim_scenario_server import CalSimScenarioClient, app
from calsim_scenario_server.database import get_db
from calsim_scenario_server.logger import logger
from calsim_scenario_server.models import Base

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
client = CalSimScenarioClient(base_url="http://localhost")
client.actor = TestClient(app)  # TODO: move this to a method


def test_testing_on_local():
    logger.debug("begin unit test")
    from pathlib import Path

    import calsim_scenario_server

    here = Path(__file__).parent
    mod_path = Path(calsim_scenario_server.__file__).parent

    rel = mod_path.relative_to(here.parent)
    assert str(rel) == "calsim_scenario_server"


def test_put_assumption():
    logger.info("begin unit test")
    assumption = client.put_assumption(
        name="example",
        kind="tucp",
        detail="foo bar baz",
    )
    assert assumption.id == 1


def test_get_assumption():
    logger.info("begin unit test")
    values = client.get_assumption(kind="tucp")
    assert len(values) == 1
    assert values[0].id == 1


def test_put_scenario():
    logger.info("begin unit test")
    assumpt_base = {"name": "add_scenario_example", "detail": "foo bar baz2"}
    assumption_names = client.get_assumption_names()
    scenario_kwargs = dict()
    for name in assumption_names:
        added = client.put_assumption(kind=name, **assumpt_base)
        scenario_kwargs[name] = added.name

    added = client.put_scenario(name="test_add_scenario", **scenario_kwargs)
    assert added.name == "test_add_scenario"


def test_get_scenario():
    logger.info("begin unit test")
    scenarios = client.get_scenario(name="test_add_scenario")
    assert len(scenarios) == 1
    scenario = scenarios[0]
    assert scenario.name == "test_add_scenario"
    assert scenario.dcp == "add_scenario_example"


# TODO: write tests for client adding runs
# TODO: write tests for client adding paths
# TODO: write tests for client addning timeseries
