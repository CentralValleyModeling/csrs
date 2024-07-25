from pathlib import Path

from csrs import clients, enums, schemas
from csrs.logger import logger

logger.setLevel("DEBUG")

TESTING_DATA = {
    "runs": [],
    "paths": [],
    "timeseries": [],
}

Client = clients.RemoteClient | clients.LocalClient


def do_assumptions(client: Client) -> list[dict[str, str]]:
    names = client.get_assumption_names()
    for n in names:
        assert n in schemas.Scenario.get_assumption_attrs()
    assumptions = [
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
    ]

    for assumption in assumptions:
        obj = client.put_assumption(**assumption)
        assert isinstance(obj, schemas.Assumption)

    array = client.get_assumption(kind=assumptions[0]["kind"])
    assert len(array) == 1
    obj = array[0]
    assert obj.detail == assumptions[0]["detail"]

    return assumptions


def test_local_assumptions(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_assumptions(client_local)


def test_remote_assumptions(client_remote: clients.remote):
    logger.debug("starting test")
    do_assumptions(client_remote)


def do_scenarios(client: Client) -> list[dict[str, str]]:
    do_assumptions(client)

    scenarios = [
        {
            "name": "testing-client-scenario-1",
            "assumptions": {
                "land_use": "testing-client-assumption-land-use",
                "sea_level_rise": "testing-client-assumption-sea-level-rise",
                "hydrology": "testing-client-assumption-hydrology-1",
                "tucp": "testing-client-assumption-tucp",
                "dcp": "testing-client-assumption-dcp",
                "va": "testing-client-assumption-va",
                "south_of_delta": "testing-client-assumption-south-of-delta",
            },
        },
        {
            "name": "testing-client-scenario-2",
            "assumptions": {
                "land_use": "testing-client-assumption-land-use",
                "sea_level_rise": "testing-client-assumption-sea-level-rise",
                "hydrology": "testing-client-assumption-hydrology-2",
                "tucp": "testing-client-assumption-tucp",
                "dcp": "testing-client-assumption-dcp",
                "va": "testing-client-assumption-va",
                "south_of_delta": "testing-client-assumption-south-of-delta",
            },
        },
    ]
    for scenario in scenarios:
        obj = client.put_scenario(**scenario)
        assert isinstance(obj, schemas.Scenario)

    array = client.get_scenario(name=scenarios[0]["name"])
    assert len(array) == 1
    obj = array[0]
    assert obj.assumptions["land_use"] == scenarios[0]["assumptions"]["land_use"]

    return scenarios


def test_local_scenarios(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_scenarios(client_local)


def test_remote_scenarios(client_remote: clients.remote):
    logger.debug("starting test")
    do_scenarios(client_remote)


def do_runs(client: Client) -> list[dict[str, str]]:
    do_scenarios(client)
    runs = [
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
    ]
    for run in runs:
        obj = client.put_run(**run)
        assert isinstance(obj, schemas.Run)

    array = client.get_run(
        scenario=runs[1]["scenario"],
        version=runs[1]["version"],
    )
    assert len(array) == 1
    obj = array[0]
    assert obj.version == runs[1]["version"]

    return runs


def test_local_runs(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_runs(client_local)


def test_remote_runs(client_remote: clients.remote):
    logger.debug("starting test")
    do_runs(client_remote)


def do_paths(client: Client) -> list[dict[str, str]]:
    paths = [
        {
            "name": "testing-client-path",
            "path": "/TESTING/PATH/CLIENT//1MON/LOCAL/",
            "category": "other",
            "period_type": "PER-AVER",
            "interval": "1MON",
            "units": "NONE",
            "detail": "Dummy path to test the API client.",
        }
    ]
    for path in paths:
        path = client.put_path(**path)
        assert isinstance(path, schemas.NamedPath)

    array = client.get_path(
        path=paths[0]["path"],
    )
    assert len(array) == 1
    obj = array[0]
    assert obj.detail == paths[0]["detail"]


def test_local_paths(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_paths(client_local)


def test_remote_paths(client_remote: clients.remote):
    logger.debug("starting test")
    do_paths(client_remote)


def do_timeseries(client: Client) -> list[dict[str, str | tuple]]:
    do_runs(client)
    do_paths(client)

    timseries = [
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
    ]
    for ts in timseries:
        client.put_timeseries(**ts)

    ts = client.get_timeseries(
        scenario=timseries[1]["scenario"],
        version=timseries[1]["version"],
        path=timseries[1]["path"],
    )
    assert isinstance(ts, schemas.Timeseries)
    assert ts.values == timseries[1]["values"]

    return timseries


def test_local_timeseries(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_timeseries(client_local)


def test_remote_timeseries(client_remote: clients.remote):
    logger.debug("starting test")
    do_timeseries(client_remote)


def do_many_timeseries(client: Client):
    runs = do_runs(client)

    paths: list[schemas.NamedPath] = [p.value for p in enums.StandardPathsEnum]
    DSS = Path(r"tests\assets\DV.dss")
    client.put_many_timeseries(
        scenario=runs[0]["scenario"],
        version=runs[0]["version"],
        dss=DSS,
        paths=paths,
    )
    for e in enums.StandardPathsEnum:
        try:
            ts = client.get_timeseries(
                scenario=runs[0]["scenario"],
                version=runs[0]["version"],
                path=e.value.name,
            )
        except Exception:
            continue
        # Accept these lenghts as these are what are in the test DV
        assert 1_200 <= len(ts.dates) <= 1_278, (
            f"{e.value.name} has the wrong size in the database: "
            + f"{len(ts.dates)}, ({len(set(ts.dates))} unique dates)"
        )


def test_local_many_timeseries(client_local: clients.LocalClient):
    logger.debug("starting test")
    do_many_timeseries(client_local)


def test_remote_many_timeseries(client_remote: clients.RemoteClient):
    logger.debug("starting test")
    do_many_timeseries(client_remote)
