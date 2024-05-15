import csrs


def test_schema_str_assumption():
    obj = csrs.schemas.Assumption(
        name="test-name",
        kind="test-kind",
        detail="test-detail",
    )
    assert "Assumption(name=test-name, kind=test-kind)" == str(obj)


def test_schema_str_scenario():
    obj = csrs.schemas.Scenario(
        name="test-name",
        land_use="test-land_use",
        sea_level_rise="test-sea_level_rise",
        hydrology="test-hydrology",
        tucp="test-tucp",
        dcp="test-dcp",
        va="test-va",
        south_of_delta="test-south_of_delta",
    )
    assert "Scenario(name=test-name, version=None)" == str(obj)


def test_schema_str_run():
    obj = csrs.schemas.Run(
        scenario="test-scenario",
        version="1.2",
        code_version="10.1",
        contact="test-contact",
        detail="test-detail",
    )
    assert "Run(scenario=test-scenario, version=1.2)" == str(obj)


def test_schema_str_timeseries():
    obj = csrs.schemas.Timeseries(
        scenario="test-scenario",
        version="1.2",
        path="/TEST/B/C//E/F/",
        values=tuple(1.0, 2.0, 3.0),
    )
    assert "Run(scenario=test-scenario, version=1.2)" == str(obj)
