from calsim_scenario_server import clients, schemas
from calsim_scenario_server.logger import logger

logger.setLevel("DEBUG")

TESTING_DATA = {
    "assumptions": [
        {
            "name": "testing-client-assumption-land-use",
            "kind": "land_use",
            "detail": "test assumption, land use",
        },
        {
            "name": "testing-client-assumption-sea-level-rise",
            "kind": "sea_level_rise",
            "detail": "test assumption, sea level rise",
        },
        # Two hydrology assumptions
        {
            "name": "testing-client-assumption-hydrology-1",
            "kind": "hydrology",
            "detail": "test assumption, hydrology 1",
        },
        {
            "name": "testing-client-assumption-hydrology-2",
            "kind": "hydrology",
            "detail": "test assumption, hydrology 2",
        },
        {
            "name": "testing-client-assumption-tucp",
            "kind": "tucp",
            "detail": "test assumption, tucp",
        },
        {
            "name": "testing-client-assumption-dcp",
            "kind": "dcp",
            "detail": "test assumption, dcp",
        },
        {
            "name": "testing-client-assumption-va",
            "kind": "va",
            "detail": "test assumption, va",
        },
        {
            "name": "testing-client-assumption-south-of-delta",
            "kind": "south_of_delta",
            "detail": "test assumption, south of delta",
        },
    ],
    "scearios": [
        {
            "name": "testing-client-scenario-1",
            "version": None,
            "land_use": "testing-client-assumption-land-use",
            "sea_level_rise": "testing-client-assumption-sea-level-rise",
            "hydrology": "testing-client-assumption-hydrology-1",
            "tucp": "testing-client-assumption-tucp",
            "dcp": "testing-client-assumption-dcp",
            "va": "testing-client-assumption-va",
            "south_of_delta": "testing-client-assumption-south-of-delta",
        },
        {
            "name": "testing-client-scenario-2",
            "version": None,
            "land_use": "testing-client-assumption-land-use",
            "sea_level_rise": "testing-client-assumption-sea-level-rise",
            "hydrology": "testing-client-assumption-hydrology-2",
            "tucp": "testing-client-assumption-tucp",
            "dcp": "testing-client-assumption-dcp",
            "va": "testing-client-assumption-va",
            "south_of_delta": "testing-client-assumption-south-of-delta",
        },
    ],
    "runs": [
        {
            "scenario": "testing-client-scenario-1",
            "version": "0.1",
            "contact": "testing@email.com",
            "code_version": "9.0.0",
            "detail": "Dummy run to test the API client. Scenario 1, is version 0.1",
        },
        {
            "scenario": "testing-client-scenario-1",
            "version": "0.2",
            "parent": "0.1",
            "contact": "update@email.com",
            "code_version": "9.0.1",
            "detail": "Dummy run to test the API client. Scenario 1, is version 0.2, "
            + "updates were made to the model code.",
        },
        {
            "scenario": "testing-client-scenario-2",
            "version": "0.1",
            "contact": "other@email.com",
            "code_version": "10.0.0",
            "confidential": False,
            "published": True,
            "detail": "Dummy run to test the API client. Scenario 2, is version 0.1",
        },
    ],
    "paths": [
        {
            "name": "testing-client-path",
            "path": "/TESTING/PATH/CLIENT//1MON/LOCAL/",
            "category": "other",
            "detail": "Dummy path to test the API client.",
        }
    ],
    "timeseries": [
        {
            "scenario": "testing-client-scenario-1",
            "version": "0.1",
            "path": "/TESTING/PATH/CLIENT//1MON/LOCAL/",
            "values": (0, 1, 2),
            "dates": ("2024-01-31", "2024-02-29", "2024-03-31"),
            "period_type": "PER-CUM",
            "units": "TAF",
            "interval": "1MON",
        },
        {
            "scenario": "testing-client-scenario-1",
            "version": "0.2",
            "path": "/TESTING/PATH/CLIENT//1MON/LOCAL/",
            "values": (3, 4, 5),
            "dates": ("2024-01-31", "2024-02-29", "2024-03-31"),
            "period_type": "PER-CUM",
            "units": "TAF",
            "interval": "1MON",
        },
        {
            "scenario": "testing-client-scenario-2",
            "version": "0.1",
            "path": "/TESTING/PATH/CLIENT//1MON/LOCAL/",
            "values": (6, 7, 8),
            "dates": ("2024-01-31", "2024-02-29", "2024-03-31"),
            "period_type": "PER-CUM",
            "units": "TAF",
            "interval": "1MON",
        },
    ],
}


def do_assumptions(client: clients.ScenarioManager):
    names = client.get_assumption_names()
    for n in names:
        assert n in schemas.Scenario.get_assumption_attrs()
    ASSUMPTIONS = TESTING_DATA["assumptions"]
    for assumption in ASSUMPTIONS:
        obj = client.put_assumption(**assumption)
        assert isinstance(obj, schemas.Assumption)

    array = client.get_assumption(kind=ASSUMPTIONS[0]["kind"])
    assert len(array) == 1
    obj = array[0]
    assert obj.detail == ASSUMPTIONS[0]["detail"]


def do_scenarios(client: clients.ScenarioManager):
    ASSUMPTIONS = TESTING_DATA["assumptions"]
    for assumption in ASSUMPTIONS:
        client.put_assumption(**assumption)

    SCENARIOS = TESTING_DATA["scearios"]
    for scenario in SCENARIOS:
        obj = client.put_scenario(**scenario)
        assert isinstance(obj, schemas.Scenario)

    array = client.get_scenario(name=SCENARIOS[0]["name"])
    assert len(array) == 1
    obj = array[0]
    assert obj.land_use == SCENARIOS[0]["land_use"]


def do_runs(client: clients.ScenarioManager):
    ASSUMPTIONS = TESTING_DATA["assumptions"]
    for assumption in ASSUMPTIONS:
        client.put_assumption(**assumption)

    SCENARIOS = TESTING_DATA["scearios"]
    for scenario in SCENARIOS:
        obj = client.put_scenario(**scenario)
        assert isinstance(obj, schemas.Scenario)

    RUNS = TESTING_DATA["runs"]
    for run in RUNS:
        obj = client.put_run(**run)
        assert isinstance(obj, schemas.Run)

    array = client.get_run(
        scenario=RUNS[1]["scenario"],
        version=RUNS[1]["version"],
    )
    assert len(array) == 1
    obj = array[0]
    assert obj.version == RUNS[1]["version"]

    # make sure scenario version was updated
    array = client.get_scenario(
        name=RUNS[1]["scenario"],
    )
    assert len(array) == 1
    obj = array[0]
    assert obj.version == RUNS[1]["version"]


def do_paths(client: clients.ScenarioManager):
    PATHS = TESTING_DATA["paths"]
    for assumption in PATHS:
        client.put_path(**assumption)

    array = client.get_path(
        path=PATHS[0]["path"],
    )
    assert len(array) == 1
    obj = array[0]
    assert obj.detail == PATHS[0]["detail"]


def do_timeseries(client: clients.ScenarioManager):
    ASSUMPTIONS = TESTING_DATA["assumptions"]
    for assumption in ASSUMPTIONS:
        client.put_assumption(**assumption)

    SCENARIOS = TESTING_DATA["scearios"]
    for scenario in SCENARIOS:
        obj = client.put_scenario(**scenario)
        assert isinstance(obj, schemas.Scenario)

    RUNS = TESTING_DATA["runs"]
    for run in RUNS:
        obj = client.put_run(**run)
        assert isinstance(obj, schemas.Run)

    PATHS = TESTING_DATA["paths"]
    for assumption in PATHS:
        client.put_path(**assumption)

    TIMESERIES = TESTING_DATA["timeseries"]
    for ts in TIMESERIES:
        client.put_timeseries(**ts)

    ts = client.get_timeseries(
        scenario=TIMESERIES[1]["scenario"],
        version=TIMESERIES[1]["version"],
        path=TIMESERIES[1]["path"],
    )
    assert isinstance(ts, schemas.Timeseries)
    assert ts.values == TIMESERIES[1]["values"]


def test_local_assumptions(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_assumptions(client_local)


def test_local_scenarios(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_scenarios(client_local)


def test_local_runs(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_runs(client_local)


def test_local_paths(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_paths(client_local)


def test_local_timeseries(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_timeseries(client_local)


def test_remote_assumptions(client_remote: clients.RemoteClient):
    logger.debug("starting test")
    do_assumptions(client_remote)


def test_remote_scenarios(client_remote: clients.RemoteClient):
    logger.debug("starting test")
    do_scenarios(client_remote)


def test_remote_runs(client_remote: clients.RemoteClient):
    logger.debug("starting test")
    do_runs(client_remote)


def test_remote_paths(client_remote: clients.RemoteClient):
    logger.debug("starting test")
    do_paths(client_remote)


def test_remote_timeseries(client_remote: clients.RemoteClient):
    logger.debug("starting test")
    do_timeseries(client_remote)
