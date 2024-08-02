import pandss as pdss
import pytest

from csrs import crud, errors, schemas


def test_create_assumpitons(database, kwargs_assumption):
    kwargs_assumption["db"] = database
    assumption = crud.assumptions.create(**kwargs_assumption)
    assert isinstance(assumption, schemas.Assumption)
    assert assumption.name == kwargs_assumption["name"]


def test_create_assumption_duplicate(database, kwargs_assumption_duplicate):
    kwargs_assumption_duplicate["db"] = database
    crud.assumptions.create(**kwargs_assumption_duplicate)
    with pytest.raises(errors.DuplicateModelError):
        crud.assumptions.create(**kwargs_assumption_duplicate)


def test_create_scenario(database, kwargs_scenario):
    kwargs_scenario["db"] = database
    scenario = crud.scenarios.create(**kwargs_scenario)
    assert scenario.name == kwargs_scenario["name"]


def test_create_run(database, kwargs_run):
    kwargs_run["db"] = database
    run = crud.runs.create(**kwargs_run)
    assert isinstance(run, schemas.Run)


def test_create_path(database, kwargs_path):
    kwargs_path["db"] = database
    path = crud.paths.create(**kwargs_path)
    assert path.name == kwargs_path["name"]


def test_read_assumpitons(database):
    objects = crud.assumptions.read(name="testing-assumption-existing", db=database)
    for obj in objects:
        assert isinstance(obj, schemas.Assumption)
    assert len(objects) == 1


def test_read_scenario(database):
    objects = crud.scenarios.read(name="testing-scenario-existing", db=database)
    for obj in objects:
        assert isinstance(obj, schemas.Scenario)
    assert len(objects) == 1


def test_read_run(database):
    objects = crud.runs.read(
        scenario="testing-scenario-existing",
        version="0.0",
        db=database,
    )
    for obj in objects:
        assert isinstance(obj, schemas.Run)
    assert len(objects) == 1


def test_read_path(database):
    objects = crud.paths.read(name="testing-path-existing", db=database)
    for obj in objects:
        assert isinstance(obj, schemas.NamedPath)
    assert len(objects) == 1


def test_read_timeseries(database):
    obj = crud.timeseries.read(
        path="/CSRS/TESTING_EXISTING_DB/TESTING/.*/1MON/2024/",
        scenario="testing-scenario-existing",
        version="0.0",
        db=database,
    )
    assert isinstance(obj, schemas.Timeseries)
    assert len(obj.values) == 1_200


def test_create_timeseries_from_dss(database, dss):
    # timeseries
    catalog = pdss.read_catalog(dss)
    for rts in pdss.read_multiple_rts(dss, catalog):
        kwargs = dict(
            scenario="testing-scenario-existing",
            version="0.0",
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


def test_error_on_bad_read_assumption(database):
    with pytest.raises(errors.EmptyLookupError):
        crud.assumptions.read(db=database, name="invalid-lookup")


def test_error_on_bad_read_scenario(database):
    with pytest.raises(errors.EmptyLookupError):
        crud.scenarios.read(db=database, name="invalid-lookup")


def test_error_on_bad_read_run(database):
    with pytest.raises(errors.EmptyLookupError):
        crud.runs.read(
            db=database,
            scenario="testing-scenario-existing",
            version="invalid-lookup",
        )


def test_error_on_bad_read_path(database):
    with pytest.raises(errors.EmptyLookupError):
        crud.paths.read(
            db=database,
            name="invalid-lookup",
        )


def test_error_on_bad_read_timeseries(database):
    with pytest.raises(errors.EmptyLookupError):
        crud.timeseries.read(
            db=database,
            scenario="testing-scenario-existing",
            version="0.0",
            path="invalid-lookup",
        )


def test_delete_assumpitons(database, kwargs_assumption):
    kwargs_assumption["db"] = database
    kwargs_assumption["name"] = "to-be-deleted"
    kwargs_assumption["detail"] = "to-be-deleted"
    assumption = crud.assumptions.create(**kwargs_assumption)
    crud.assumptions.delete(database, assumption.id)
    with pytest.raises(errors.EmptyLookupError):
        crud.assumptions.read(database, name="to-be-deleted")


def test_delete_scenario(database, kwargs_scenario):
    kwargs_scenario["db"] = database
    kwargs_scenario["name"] = "to-be-deleted"
    scenario = crud.scenarios.create(**kwargs_scenario)
    crud.scenarios.delete(database, scenario.id)
    with pytest.raises(errors.EmptyLookupError):
        crud.scenarios.read(database, name="to-be-deleted")


def test_delete_run(database, kwargs_run):
    kwargs_run["db"] = database
    kwargs_run["version"] = "to-be-deleted"
    run = crud.runs.create(**kwargs_run)
    crud.runs.delete(database, run.id)
    with pytest.raises(errors.EmptyLookupError):
        crud.runs.read(database, version="to-be-deleted")


def test_delete_path(database, kwargs_path):
    kwargs_path["db"] = database
    kwargs_path["name"] = "to-be-deleted"
    path = crud.paths.create(**kwargs_path)
    crud.paths.delete(database, path.id)
    with pytest.raises(errors.EmptyLookupError):
        crud.paths.read(database, name="to-be-deleted")


# TODO: add tests for different length timeseries
# TODO: add tests for adding two runs in a scenario, updating the preferred run
