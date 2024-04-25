from pathlib import Path
from re import sub
from unicodedata import normalize

import pandss as pdss
from sqlalchemy.orm import Session

from .. import models, schemas
from ..errors import LookupUniqueError
from .decorators import rollback_on_exception


def safe_file_name(s: str) -> str:
    s = normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = sub(r"[^\w\s-]", "", s).strip().lower()
    s = sub(r"[-\s]+", "_", s)
    return s


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
    path: str | pdss.DatasetPath,
    values: tuple[float],
    dates: tuple[str],
    period_type: str,
    units: str,
    interval: str,
) -> schemas.Timeseries:
    # Get the scenario, and the run we are adding data to
    sceanrio_model = (
        db.query(models.Scenario).filter(models.Scenario.name == scenario).first()
    )
    run = sceanrio_model.run
    if run.version != version:
        # Adding data to an older version
        run = get_run_model(db, scenario=scenario, version=version)
    # Check if run has a DSS yet
    dss = run.dss
    if dss is None:
        s = safe_file_name(sceanrio_model.name)
        r = safe_file_name(run.version)
        dss = str(get_dss_root(db) / f"{s}_{r}.dss")
        run.dss = dss
    # Get the path model
    if not isinstance(path, pdss.DatasetPath):
        path = pdss.DatasetPath.from_str(path)
    path_model = (
        db.query(models.NamedPath).filter(models.NamedPath.path == str(path)).first()
    )
    if path_model is None:
        raise LookupUniqueError(models.NamedPath, path_model, path=repr(path))
    # Add the timeseries to the common catalog
    catalog_row = models.CommonCatalog(dss=dss, path_id=path_model.id)
    db.add(catalog_row)
    # Put the data into the DSS
    rts = pdss.RegularTimeseries.from_json(
        dict(
            path=str(path),  # TODO: update pandss to handle types better on from_json
            values=values,
            dates=dates,
            period_type=period_type,
            units=units,
            interval=interval,
        )
    )
    dss_obj = pdss.DSS(dss)
    with dss_obj:
        dss_obj.write_rts(path, rts)

    timeseries = schemas.Timeseries(scenario=scenario, version=version, **rts.to_json())

    db.commit()

    return timeseries


@rollback_on_exception
def read(
    db: Session,
    scenario: str,
    version: str,
    path: str | pdss.DatasetPath,
) -> schemas.Timeseries:
    # Get the scenario, and the run we are adding data to
    sceanrio_model = (
        db.query(models.Scenario).filter(models.Scenario.name == scenario).first()
    )
    run = sceanrio_model.run
    if run.version != version:
        # Adding data to an older version
        run = get_run_model(db, scenario=scenario, version=version)
    # Check if run has a DSS yet
    dss = run.dss
    if not dss:
        raise LookupUniqueError(models.Run, run, dss=pdss.DSS)
    elif not Path(dss).exists():
        raise FileNotFoundError(dss)
    if not isinstance(path, pdss.DatasetPath):
        path = pdss.DatasetPath.from_str(path)
    with pdss.DSS(dss) as dss_obj:
        rts = dss_obj.read_rts(path)

    return schemas.Timeseries(scenario=scenario, version=version, **rts.to_json())


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
