from pathlib import Path

import pandss as pdss
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from csrs import crud, enums, errors, models, schemas

TEST_ASSETS_DIR = Path(__file__).parent / "assets"
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)
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
    with pytest.raises(errors.DuplicateAssumptionError):
        crud.assumptions.create(**kwargs)


def test_create_scenario():
    default_assumption_kwargs = dict(
        name="testing-create-scenario",
        detail="testing create scenario",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-create-scenario",
        version="0.1",
        db=session,
    )
    for kind in enums.AssumptionEnum:
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
    for kind in enums.AssumptionEnum:
        if kind.value == "dcp":
            continue
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-create-scenario-incomplete",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        if kind.value == "dcp":
            continue
        kwargs[kind.value] = default_assumption_kwargs["name"]
    with pytest.raises(errors.ScenarioAssumptionError):
        crud.scenarios.create(**kwargs)


def test_update_scenario_version():
    default_assumption_kwargs = dict(
        name="testing-update-scenario-assumption",
        detail="testing update scenario",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-update-scenario",
        version="0.1",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        kwargs[kind.value] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)

    # Create run
    kwargs = dict(
        scenario="testing-update-scenario",
        version="0.2",
        contact="user@email.com",
        code_version="0.1",
        detail="testing update scenario",
        db=session,
    )
    crud.runs.create(**kwargs)

    # See if the version was updated
    (scenario,) = crud.scenarios.read(db=session, name=kwargs["scenario"])
    assert scenario.version == kwargs["version"]


def test_create_run():
    default_assumption_kwargs = dict(
        name="testing-create-run-assumption",
        detail="testing create run",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)
    # Create scenario
    kwargs = dict(
        name="testing-create-run-scenario",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        kwargs[kind.value] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)
    # Create run
    kwargs = dict(
        scenario="testing-create-run-scenario",
        version="0.2",
        contact="user@email.com",
        code_version="0.1",
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
    for kind in enums.AssumptionEnum:
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-read-run-scenario",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        kwargs[kind.value] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)

    kwargs = dict(
        scenario="testing-read-run-scenario",
        code_version="0.1",
        contact="user@email.com",
        version="0.2",
        parent=None,
        detail="testing read run",
        db=session,
    )
    crud.runs.create(**kwargs)
    runs = crud.runs.read(db=session, scenario="testing-read-run-scenario")
    assert len(runs) == 1
    run = runs[0]
    assert run.scenario == "testing-read-run-scenario"
    assert len(run.children) == 0
    assert run.parent is None


def test_create_path():
    kwargs = dict(
        name="shasta-storage-test-create-path",
        path="/.*/S_SHSTA/STORAGE/.*/.*/.*/",
        category="storage",
        period_type="PER-AVER",
        interval="1MON",
        units="TAF",
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
        period_type="PER-AVER",
        interval="1MON",
        units="TAF",
        detail="The storage in Oroville Reservoir, in TAF.",
        db=session,
    )
    crud.paths.create(**kwargs)
    paths = crud.paths.read(db=session, path=kwargs["path"])
    assert len(paths) == 1
    path = paths[0]
    assert path.name == kwargs["name"]


def test_create_read_timeseries():
    # assumptions
    default_assumption_kwargs = dict(
        name="testing-create-timeseries-assumption",
        detail="testing create timeseries",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        crud.assumptions.create(kind=kind.value, **default_assumption_kwargs)
    # scenario
    kwargs = dict(
        name="testing-create-timeseries-scenario",
        db=session,
    )
    for kind in enums.AssumptionEnum:
        kwargs[kind.value] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)
    # run
    kwargs = dict(
        scenario="testing-create-timeseries-scenario",
        code_version="0.1",
        contact="user@email.com",
        version="0.2",
        parent=None,
        detail="testing-create-timeseries",
        db=session,
    )
    crud.runs.create(**kwargs)
    # path
    kwargs = dict(
        name="shasta-sotrage-test-read-timeseries",
        path="/CALSIM/S_SHSTA/STORAGE//1MON/L2020A/",
        category="storage",
        detail="Storage in Shasta Reservoir in TAF.",
        db=session,
    )
    crud.paths.create(**kwargs)
    # timeseries
    dss = TEST_ASSETS_DIR / "DV.dss"
    path = pdss.DatasetPath.from_str(kwargs["path"])
    rts = pdss.read_rts(dss, path)
    assert isinstance(rts, pdss.RegularTimeseries)

    kwargs = dict(
        scenario="testing-create-timeseries-scenario",
        version="0.2",
        **rts.to_json(),
        db=session,
    )
    timeseries = crud.timeseries.create(**kwargs)
    assert isinstance(timeseries, schemas.Timeseries)
    assert timeseries.values[0] == float(rts.values[0])
    assert len(timeseries.values) == len(rts.values)
    rts_2 = pdss.RegularTimeseries.from_json(
        timeseries.model_dump(exclude=("id", "scenario", "version"))
    )
    for L, R in zip(rts.dates, rts_2.dates):
        assert L == R

    timeseries_read = crud.timeseries.read(
        db=session,
        scenario=kwargs["scenario"],
        version=kwargs["version"],
        path=kwargs["path"],
    )
    assert timeseries.path == timeseries_read.path
    for L, R in zip(timeseries.values, timeseries_read.values):
        assert L == R


# TODO: add tests for hard to convert scenario names (for dss file name)
# TODO: add tests for different length timeseries
# TODO: add tests for adding two runs in a scenario, updating the preferred run
