import pandss as pdss
import pytest

from csrs import crud, errors, schemas


def test_create_assumpitons(database):
    kwargs = dict(
        name="testing-create-assumption",
        kind="tucp",
        detail="testing assumption, tucp as placeholder",
        db=database,
    )
    assumption = crud.assumptions.create(**kwargs)
    assert isinstance(assumption, schemas.Assumption)
    assert assumption.name == kwargs["name"]


def test_read_assumpitons(database):
    kwargs = dict(
        name="testing-read-assumption",
        kind="tucp",
        detail="testing read assumption, tucp as placeholder",
        db=database,
    )
    crud.assumptions.create(**kwargs)
    assumptions = crud.assumptions.read(name=kwargs["name"], db=kwargs["db"])
    for assumption in assumptions:
        assert isinstance(assumption, schemas.Assumption)
        assert assumption.name == kwargs["name"]


def test_create_assumption_duplicate(database):
    kwargs = dict(
        name="testing-create-assumption-failure-duplicate",
        kind="hydrology",
        detail="testing duplicate assumption",
        db=database,
    )
    crud.assumptions.create(**kwargs)
    with pytest.raises(errors.DuplicateModelError):
        crud.assumptions.create(**kwargs)


def test_create_scenario(database):
    default_assumption_kwargs = dict(
        name="testing-create-scenario",
        detail="testing create scenario",
        db=database,
    )
    test_kinds = ("assumption-kind-1", "assumption-kind-2", "assumption-kind-3")
    for kind in test_kinds:
        crud.assumptions.create(kind=kind, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-create-scenario",
        assumptions=dict(),
        db=database,
    )
    for kind in test_kinds:
        kwargs["assumptions"][kind] = default_assumption_kwargs["name"]
    scenario = crud.scenarios.create(**kwargs)
    assert scenario.name == kwargs["name"]
    assert scenario.assumptions[test_kinds[0]] == default_assumption_kwargs["name"]


def test_create_run(database):
    default_assumption_kwargs = dict(
        name="testing-create-run-assumption",
        detail="testing create run",
        db=database,
    )
    test_kinds = ("assumption-kind-1", "assumption-kind-2", "assumption-kind-3")
    for kind in test_kinds:
        crud.assumptions.create(kind=kind, **default_assumption_kwargs)
    # Create scenario
    kwargs = dict(
        name="testing-create-run-scenario",
        assumptions=dict(),
        db=database,
    )
    for kind in test_kinds:
        kwargs["assumptions"][kind] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)
    # Create run
    kwargs = dict(
        scenario="testing-create-run-scenario",
        version="0.2",
        contact="user@email.com",
        code_version="0.1",
        detail="testing-create-run",
        db=database,
    )
    run = crud.runs.create(**kwargs)
    assert isinstance(run, schemas.Run)


def test_read_run(database):
    default_assumption_kwargs = dict(
        name="testing-read-run-assumption",
        detail="testing read run",
        db=database,
    )
    test_kinds = ("assumption-kind-1", "assumption-kind-2", "assumption-kind-3")
    for kind in test_kinds:
        crud.assumptions.create(kind=kind, **default_assumption_kwargs)

    kwargs = dict(
        name="testing-read-run-scenario",
        assumptions=dict(),
        db=database,
    )
    for kind in test_kinds:
        kwargs["assumptions"][kind] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)

    kwargs = dict(
        scenario="testing-read-run-scenario",
        code_version="0.1",
        contact="user@email.com",
        version="0.2",
        parent=None,
        detail="testing read run",
        db=database,
    )
    crud.runs.create(**kwargs)
    runs = crud.runs.read(db=database, scenario="testing-read-run-scenario")
    assert len(runs) == 1
    run = runs[0]
    assert run.scenario == "testing-read-run-scenario"
    assert len(run.children) == 0
    assert run.parent is None


def test_create_path(database):
    kwargs = dict(
        name="shasta-storage-test-create-path",
        path="/.*/S_SHSTA/STORAGE/.*/.*/.*/",
        category="storage",
        period_type="PER-AVER",
        interval="1MON",
        units="TAF",
        detail="The storage in Shasta Reservoir, in TAF.",
        db=database,
    )
    path = crud.paths.create(**kwargs)
    assert path.name == kwargs["name"]


def test_read_path(database):
    kwargs = dict(
        name="Oroville Storage",
        path="/.*/S_OROVL/STORAGE/.*/.*/.*/",
        category="storage",
        period_type="PER-AVER",
        interval="1MON",
        units="TAF",
        detail="The storage in Oroville Reservoir, in TAF.",
        db=database,
    )
    crud.paths.create(**kwargs)
    paths = crud.paths.read(db=database, path=kwargs["path"])
    assert len(paths) == 1
    path = paths[0]
    assert path.name == kwargs["name"]


def test_create_read_timeseries(database, assets_dir):
    # assumptions
    default_assumption_kwargs = dict(
        name="testing-create-timeseries-assumption",
        detail="testing create timeseries",
        db=database,
    )
    test_kinds = ("assumption-kind-1", "assumption-kind-2", "assumption-kind-3")
    for kind in test_kinds:
        crud.assumptions.create(kind=kind, **default_assumption_kwargs)
    # scenario
    kwargs = dict(
        name="testing-create-timeseries-scenario",
        assumptions=dict(),
        db=database,
    )
    for kind in test_kinds:
        kwargs["assumptions"][kind] = default_assumption_kwargs["name"]
    crud.scenarios.create(**kwargs)
    # run
    kwargs = dict(
        scenario="testing-create-timeseries-scenario",
        code_version="0.1",
        contact="user@email.com",
        version="0.2",
        parent=None,
        detail="testing-create-timeseries",
        db=database,
    )
    crud.runs.create(**kwargs)
    # path
    kwargs = dict(
        name="shasta-sotrage-test-read-timeseries",
        path="/CALSIM/S_SHSTA/STORAGE/.*/1MON/L2020A/",
        category="storage",
        period_type="PER-AVER",
        interval="1MON",
        units="TAF",
        detail="Storage in Shasta Reservoir in TAF.",
        db=database,
    )
    crud.paths.create(**kwargs)
    # timeseries
    dss = assets_dir / "DV.dss"
    path = pdss.DatasetPath.from_str(kwargs["path"])
    rts = pdss.read_rts(dss, path)
    assert isinstance(rts, pdss.RegularTimeseries)

    kwargs = dict(
        scenario="testing-create-timeseries-scenario",
        version="0.2",
        **rts.to_json(),
        db=database,
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
        db=database,
        scenario=kwargs["scenario"],
        version=kwargs["version"],
        path=kwargs["path"],
    )
    assert timeseries.path == timeseries_read.path
    for L, R in zip(timeseries.dates, timeseries_read.dates):
        assert L == R


# TODO: add tests for hard to convert scenario names (for dss file name)
# TODO: add tests for different length timeseries
# TODO: add tests for adding two runs in a scenario, updating the preferred run
