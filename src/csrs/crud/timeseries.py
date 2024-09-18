import logging
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy.orm import Session

from .. import models, schemas
from ..errors import EmptyLookupError, UniqueLookupError
from . import paths as crud_paths
from ._common import rollback_on_exception

logger = logging.getLogger(__name__)
EPOCH = datetime(1900, 1, 1)


def date_to_float(date: str) -> float:
    dt: timedelta = datetime.fromisoformat(date) - EPOCH
    return dt.total_seconds()


def float_to_date(date: float) -> str:
    dt: datetime = EPOCH + timedelta(seconds=date)
    return dt.isoformat()


def get_dss_root(db: Session) -> Path:
    path = None
    if db.bind.dialect.name == "sqlite":
        db_path = db.bind.url.database
        if db_path and (":memory:" not in db_path):
            try:
                path = Path(db.bind.url.database).parent
            except Exception:
                path = None
    if path is None:
        path = Path("./dss").resolve()

    path.mkdir(parents=False, exist_ok=True)
    return path


def get_run_model(db: Session, scenario: str, version: str) -> models.Run:
    # TODO: 2024-07-30 See if we can remove this function in favor of crud.runs.read
    if not isinstance(scenario, str):
        raise ValueError(f"{scenario=}, expected str")
    scenario_model = (
        db.query(models.Scenario).filter(models.Scenario.name == scenario).first()
    )
    runs = (
        db.query(models.Run).filter(models.Run.scenario_id == scenario_model.id).all()
    )
    runs = [r for r in runs if r.version == version]
    if len(runs) == 0:  # Couldn't find version
        raise EmptyLookupError(models.Run, version=version, scenario=scenario)
    return runs[0]


@rollback_on_exception
def create(
    db: Session,
    scenario: str,
    version: str,
    path: str,
    values: tuple[float],
    dates: tuple[str],
    **kwargs,
) -> schemas.Timeseries:
    logger.info(f"creating new timeseries for {scenario=}, {version=} {path=}")

    # ignore certain kwargs
    for k in ("period_type", "interval", "units"):
        kwargs.pop(k)
    if kwargs:
        raise TypeError(f"create() got unexpected keyword arguments: {kwargs.keys()}")
    # Validation
    if len(dates) != len(values):
        raise ValueError(
            "dates and values must be 1:1\n"
            + f"\t{len(dates)=}\n"
            + f"\t{len(values)=}"
        )
    # Get the scenario, and the run we are adding data to
    sceanrio_model = (
        db.query(models.Scenario).filter(models.Scenario.name == scenario).first()
    )
    run_model = sceanrio_model.run
    if run_model is None:
        raise ValueError(f"Run {scenario} (v{version}) does not exist in the database")
    elif run_model.version != version:
        # Adding data to an older version
        run_model = get_run_model(db, scenario=scenario, version=version)
    # Get the path model
    path_schemas = crud_paths.read(db=db, path=path)
    if not path_schemas:
        path_schemas = crud_paths.read(db=db, name=path)
    if len(path_schemas) > 1:
        raise UniqueLookupError(models.NamedPath, path_schemas, path=repr(path))
    dss_path = path_schemas[0].path
    path_model = (
        db.query(models.NamedPath).filter(models.NamedPath.path == dss_path).first()
    )
    # Add the timeseries to the common catalog
    catalog_row = models.CommonCatalog(run_id=run_model.id, path_id=path_model.id)
    db.add(catalog_row)
    # Put the data into the database
    dates_float = (date_to_float(d) for d in dates)
    objects = (
        models.TimeseriesLedger(
            run_id=run_model.id,
            path_id=path_model.id,
            datetime=d,
            value=values[i],
        )
        for i, d in enumerate(dates_float)
    )
    db.add_all(objects)
    db.commit()

    ts = schemas.Timeseries(
        scenario=sceanrio_model.name,
        version=run_model.version,
        path=path_model.path,
        values=list(values),
        dates=list(dates),
        period_type=path_model.period_type,
        units=path_model.units,
        interval=path_model.interval,
    )

    return ts


@rollback_on_exception
def read(
    db: Session,
    scenario: str,
    version: str,
    path: str,
) -> schemas.Timeseries:
    logger.info(f"reading timeseries where {scenario=}, {version=} {path=}")
    # Get the scenario, and the run we are adding data to
    sceanrio_model = (
        db.query(models.Scenario).filter(models.Scenario.name == scenario).first()
    )
    run = sceanrio_model.run
    if run.version != version:
        # Adding data to an older version
        run = get_run_model(db, scenario=scenario, version=version)
    # Get the path model
    path_schemas = crud_paths.read(db=db, path=path)
    if not path_schemas:
        path_schemas = crud_paths.read(db=db, name=path)
    if len(path_schemas) == 0:
        raise EmptyLookupError(models.NamedPath, path=repr(path))
    path_schema = path_schemas[0]
    # Get data from database
    rows = (
        db.query(models.TimeseriesLedger)
        .filter(
            models.TimeseriesLedger.run_id == run.id,
            models.TimeseriesLedger.path_id == path_schema.id,
        )
        .all()
    )
    logger.info(f"{len(rows):,} rows found matching criteria")
    dates = tuple(float_to_date(r.datetime) for r in rows)
    values = tuple(r.value for r in rows)

    return schemas.Timeseries(
        scenario=scenario,
        version=version,
        path=path_schema.path,
        units=path_schema.units,
        period_type=path_schema.period_type,
        interval=path_schema.interval,
        dates=dates,
        values=values,
    )


@rollback_on_exception
def read_all_for_run(
    db: Session,
    scenario: str,
    version: str,
) -> list[schemas.Timeseries]:
    logger.info(f"reading all timeseries where {scenario=}, {version=}")
    # Get the scenario, and the run we are adding data to
    sceanrio_model = (
        db.query(models.Scenario).filter(models.Scenario.name == scenario).first()
    )
    run = sceanrio_model.run
    if (run is None) or (run.version != version):
        # Adding data to an older version
        run = get_run_model(db, scenario=scenario, version=version)

    # Get data from database
    rows = (
        db.query(models.TimeseriesLedger)
        .filter(
            models.TimeseriesLedger.run_id == run.id,
        )
        .order_by(models.TimeseriesLedger.path_id)
        .all()
    )
    logger.info(f"{len(rows):,} rows found matching criteria")
    # Construct the schemas from the returned data
    paths = crud_paths.read_paths_in_run(db, run_id=run.id)
    paths_by_id = {p.id: p for p in paths}
    grouped_rows: dict[int, list[models.TimeseriesLedger]] = {
        row.path_id: list() for row in rows
    }
    for row in rows:
        grouped_rows[row.path_id].append(row)
    timeseries = list()
    for path_id, rows in grouped_rows.items():
        if path_id not in paths_by_id:
            logger.warning(f"{path_id=} not found for run")
            path_schemas = crud_paths.read(db, id=path_id)
            if len(path_schemas) != 1:
                raise UniqueLookupError(models.NamedPath, path_schemas, id=path_id)
            path_schema = path_schemas[0]
        else:
            path_schema = paths_by_id[path_id]
        values = tuple(r.value for r in rows)
        dates = tuple(float_to_date(r.datetime) for r in rows)
        timeseries.append(
            schemas.Timeseries(
                scenario=scenario,  # always the same
                version=version,  # always the same
                path=path_schema.path,
                units=path_schema.units,
                period_type=path_schema.period_type,
                interval=path_schema.interval,
                dates=dates,
                values=values,
            )
        )

    return timeseries


def update():
    raise NotImplementedError()


@rollback_on_exception
def delete(db: Session, scenario: str, version: str, path: str) -> int:
    statement = (
        db.query(models.TimeseriesLedger)
        .join(models.Run)
        .join(models.Scenario)
        .where(models.Scenario.name == scenario)
        .where(models.Run.version == version)
        .join(models.NamedPath)
        .where(models.NamedPath.path == path)
    )
    objs = statement.all()
    if len(objs) == 0:
        raise EmptyLookupError(
            models.TimeseriesLedger,
            sceanrio=scenario,
            version=version,
            path=path,
        )
    n_deleted = len(objs)
    statement.delete(synchronize_session="auto")
    db.commit()
    return n_deleted
