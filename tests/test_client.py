from pathlib import Path

from csrs import clients, schemas
from csrs.logger import logger

Client = clients.RemoteClient | clients.LocalClient


def do_assumptions(
    client: Client,
    kwargs_assumption: dict[str, str],
):

    obj = client.put_assumption(**kwargs_assumption)
    assert isinstance(obj, schemas.Assumption)

    array = client.get_assumption(name=kwargs_assumption["name"])
    assert len(array) == 1
    obj = array[0]
    assert obj.detail == kwargs_assumption["detail"]


def test_local_assumptions(
    client_local: clients.LocalClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_assumptions(client_local, kwargs_all_unique["assumption"])


def test_remote_assumptions(
    client_remote: clients.RemoteClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_assumptions(client_remote, kwargs_all_unique["assumption"])


def do_scenarios(
    client: Client,
    kwargs_scenario: dict[str, str],
):
    obj = client.put_scenario(**kwargs_scenario)
    assert isinstance(obj, schemas.Scenario)
    array = client.get_scenario(name=obj.name)
    assert len(array) == 1


def test_local_scenarios(
    client_local: clients.LocalClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_scenarios(client_local, kwargs_all_unique["scenario"])


def test_remote_scenarios(
    client_remote: clients.RemoteClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_scenarios(client_remote, kwargs_all_unique["scenario"])


def do_runs(
    client: Client,
    kwargs_run: dict[str, str],
):
    obj = client.put_run(**kwargs_run)
    assert isinstance(obj, schemas.Run)
    array = client.get_run(
        scenario=kwargs_run["scenario"],
        version=kwargs_run["version"],
    )
    assert len(array) == 1
    obj2 = array[0]
    assert obj2.version == kwargs_run["version"]


def test_local_runs(
    client_local: clients.LocalClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_runs(client_local, kwargs_all_unique["run"])


def test_remote_runs(
    client_remote: clients.RemoteClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_runs(client_remote, kwargs_all_unique["run"])


def do_paths(
    client: Client,
    kwargs_path: dict[str, str],
):
    path = client.put_path(**kwargs_path)
    assert isinstance(path, schemas.NamedPath)

    array = client.get_path(
        path=kwargs_path["path"],
    )
    assert len(array) == 1
    obj2 = array[0]
    assert obj2.detail == kwargs_path["detail"]


def test_local_paths(
    client_local: clients.LocalClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_paths(client_local, kwargs_all_unique["path"])


def test_remote_paths(
    client_remote: clients.RemoteClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_paths(client_remote, kwargs_all_unique["path"])


def do_timeseries(
    client: Client,
    kwargs_timeseries: dict[str, str],
    kwargs_run: dict[str, str],
):
    client.put_run(**kwargs_run)  # must add a new run to make sure the ts is unique
    client.put_timeseries(**kwargs_timeseries)
    ts = client.get_timeseries(
        scenario=kwargs_timeseries["scenario"],
        version=kwargs_timeseries["version"],
        path=kwargs_timeseries["path"],
    )
    assert isinstance(ts, schemas.Timeseries)
    assert ts.values == kwargs_timeseries["values"]


def test_local_timeseries(
    client_local: clients.LocalClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_timeseries(
        client_local,
        kwargs_all_unique["timeseries"],
        kwargs_all_unique["run"],
    )


def test_remote_timeseries(
    client_remote: clients.RemoteClient,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_timeseries(
        client_remote,
        kwargs_all_unique["timeseries"],
        kwargs_all_unique["run"],
    )


def do_many_timeseries(
    client: Client,
    dss: Path,
    kwargs_timeseries: dict[str, str],
    kwargs_run: dict[str, str],
):
    client.put_run(**kwargs_run)  # must add a new run to make sure the ts is unique
    all_ts = client.put_many_timeseries(
        scenario=kwargs_timeseries["scenario"],
        version=kwargs_timeseries["version"],
        dss=dss,
    )
    for ts in all_ts:
        assert isinstance(ts, schemas.Timeseries)
        assert len(ts.dates) == len(ts.values)
        assert len(ts.values) > 0
        assert isinstance(ts.values[0], float)


def test_local_many_timeseries(
    client_local: clients.RemoteClient,
    dss: Path,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_many_timeseries(
        client_local,
        dss,
        kwargs_all_unique["timeseries"],
        kwargs_all_unique["run"],
    )


def test_remote_many_timeseries(
    client_remote: clients.RemoteClient,
    dss: Path,
    kwargs_all_unique: dict[str, dict[str, str]],
):
    logger.debug("starting test")
    do_many_timeseries(
        client_remote,
        dss,
        kwargs_all_unique["timeseries"],
        kwargs_all_unique["run"],
    )
