import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from calsim_scenario_server import crud, enum, schemas
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
session = TestingSessionLocal()


def test_create_assumpitons():
    kwargs = dict(
        name="testing-create-assumption",
        kind="tucp",
        detail="testing assumption, tucp as placeholder",
        db=session,
    )
    assumption = crud.assumptions.create(**kwargs)
    assert isinstance(assumption, schemas.Assumption)
    assert assumption.name == kwargs["name"]


def test_read_assumpitons():
    kwargs = dict(
        name="testing-read-assumption",
        kind="tucp",
        detail="testing read assumption, tucp as placeholder",
        db=session,
    )
    crud.assumptions.create(**kwargs)
    assumptions = crud.assumptions.read(name=kwargs["name"], db=kwargs["db"])
    for assumption in assumptions:
        assert isinstance(assumption, schemas.Assumption)
        assert assumption.name == kwargs["name"]


def test_create_assumption_bad_enum():
    kwargs = dict(
        name="testing-create-assumption-failure-enum",
        kind="bad-enum-type",
        detail="testing bad assumption enum",
        db=session,
    )
    with pytest.raises(LookupError):
        crud.assumptions.create(**kwargs)


def test_create_assumption_duplicate():
    kwargs = dict(
        name="testing-create-assumption-failure-duplicate",
        kind="hydrology",
        detail="testing duplicate assumption",
        db=session,
    )
    crud.assumptions.create(**kwargs)
    with pytest.raises(AttributeError):
        crud.assumptions.create(**kwargs)


def test_create_scenario():
    default_assumption_kwargs = dict(
        name="testing-create-scenario",
        detail="testing create scenario",
        db=session,
    )
    for kind in enum.AssumptionEnum:
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-create-scenario",
        db=session,
    )
    for kind in enum.AssumptionEnum:
        kwargs[kind.value] = default_assumption_kwargs["name"]
    scenario = crud.scenarios.create(**kwargs)
    assert scenario.name == kwargs["name"]
    assert scenario.hydrology == default_assumption_kwargs["name"]


def test_create_scenario_incomplete_assumption_specification():
    default_assumption_kwargs = dict(
        name="testing-create-scenario-incomplete",
        detail="testing create scenario with not all assumptions",
        db=session,
    )
    for kind in enum.AssumptionEnum:
        if kind.value == "dcp":
            continue
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-create-scenario-incomplete",
        db=session,
    )
    for kind in enum.AssumptionEnum:
        if kind.value == "dcp":
            continue
        kwargs[kind.value] = default_assumption_kwargs["name"]
    with pytest.raises(AttributeError):
        crud.scenarios.create(**kwargs)


def test_create_run():
    default_assumption_kwargs = dict(
        name="testing-create-run-assumption",
        detail="testing create run",
        db=session,
    )
    for kind in enum.AssumptionEnum:
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-create-run-scenario",
        db=session,
    )
    for kind in enum.AssumptionEnum:
        kwargs[kind.value] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)

    kwargs = dict(
        scenario="testing-create-run-scenario",
        code_version="0.1",
        contact="user@email.com",
        version="0.2",
        predecessor_run_name=None,
        detail="testing-create-run",
        db=session,
    )
    crud.runs.create(**kwargs)


def test_read_run():
    default_assumption_kwargs = dict(
        name="testing-read-run-assumption",
        detail="testing read run",
        db=session,
    )
    for kind in enum.AssumptionEnum:
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-read-run-scenario",
        db=session,
    )
    for kind in enum.AssumptionEnum:
        kwargs[kind.value] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)

    kwargs = dict(
        scenario="testing-read-run-scenario",
        code_version="0.1",
        contact="user@email.com",
        version="0.2",
        predecessor_run_name=None,
        detail="testing read run",
        db=session,
    )
    crud.runs.create(**kwargs)
    runs = crud.runs.read(db=session, scenario="testing-read-run-scenario")
    assert len(runs) == 1
    run = runs[0]
    assert run.scenario == "testing-read-run-scenario"
    assert len(run.children_ids) == 0
    assert run.parent_id is None


def test_create_path():
    kwargs = dict(
        name="Shasta Storage",
        path="/.*/S_SHSTA/STORAGE/.*/.*/.*/",
        category="storage",
        detail="The storage in Shasta Reservoir, in TAF.",
        db=session,
    )
    path = crud.paths.create(**kwargs)
    assert path.name == kwargs["name"]


def test_read_path():
    kwargs = dict(
        name="Oroville Storage",
        path="/.*/S_OROVL/STORAGE/.*/.*/.*/",
        category="storage",
        detail="The storage in Oroville Reservoir, in TAF.",
        db=session,
    )
    crud.paths.create(**kwargs)
    paths = crud.paths.read(db=session, path=kwargs["path"])
    assert len(paths) == 1
    path = paths[0]
    assert path.name == kwargs["name"]


def test_create_timeseries_values():
    kwargs = dict(
        datetime_str="1921-10-31T23:59:00",
        db=session,
    )
    ts = crud.timeseries.create(**kwargs)
    assert ts.datetime_str == kwargs["datetime_str"]


def test_read_timeseries_values():
    kwargs = dict(
        datetime_str="1921-10-31T23:59:00",
        db=session,
    )
    crud.timeseries.create(**kwargs)
    tss = crud.timeseries.read(**kwargs)
    assert len(tss) == 1
    ts = tss[0]
    assert ts.datetime_str == kwargs["datetime_str"]
