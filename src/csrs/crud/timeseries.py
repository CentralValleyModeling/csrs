from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import EPOCH
from ..errors import LookupUniqueError
from ..logger import logger
from .decorators import rollback_on_exception


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
    if not isinstance(scenario, str):
        raise ValueError(f"{scenario=}, expected str")
    scenario_model = (
        db.query(models.Scenario).filter(models.Scenario.name == scenario).first()
    )
    runs = (
        db.query(models.Run).filter(models.Run.scenario_id == scenario_model.id).all()
    )
    runs = [r for r in runs if r.version == version]
    if len(runs) != 1:  # Couldn't find version
        raise LookupUniqueError(models.Run, runs, version=version, scenario=scenario)
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
    if run_model.version != version:
        # Adding data to an older version
        run_model = get_run_model(db, scenario=scenario, version=version)
    # Get the path model
    path_model = (
        db.query(models.NamedPath).filter(models.NamedPath.path == str(path)).first()
    )
    if path_model is None:
        raise LookupUniqueError(models.NamedPath, path_model, path=repr(path))
    # Add the timeseries to the common catalog
    catalog_row = models.CommonCatalog(run_id=run_model.id, path_id=path_model.id)
    db.add(catalog_row)
    # Put the data into the database
    dates = (date_to_float(d) for d in dates)
    objects = (
        models.TimeseriesLedger(
            run_id=run_model.id,
            path_id=path_model.id,
            datetime=d,
            value=values[i],
        )
        for i, d in enumerate(dates)
    )
    db.add_all(objects)
    db.commit()

    ts = schemas.Timeseries(
        scenario=sceanrio_model.name,
        version=run_model.version,
        path=path_model.path,
        values=list(values),
        dates=list(float_to_date(d) for d in dates),
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
    path_model = (
        db.query(models.NamedPath).filter(models.NamedPath.path == str(path)).first()
    )
    if path_model is None:
        raise LookupUniqueError(models.NamedPath, path_model, path=repr(path))
    # Get data from database
    rows = (
        db.query(models.TimeseriesLedger)
        .filter(
            models.TimeseriesLedger.run_id == run.id,
            models.TimeseriesLedger.path_id == path_model.id,
        )
        .all()
    )
    logger.info(f"{len(rows):,} rows found matching criteria")
    dates = tuple(float_to_date(r.datetime) for r in rows)
    values = tuple(r.value for r in rows)

    return schemas.Timeseries(
        scenario=scenario,
        version=version,
        path=path_model.path,
        units=path_model.units,
        period_type=path_model.period_type,
        interval=path_model.interval,
        dates=dates,
        values=values,
    )


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
