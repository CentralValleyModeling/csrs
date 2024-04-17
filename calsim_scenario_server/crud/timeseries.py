from re import sub
from unicodedata import normalize

import pandss as pdss
from sqlalchemy.orm import Session

from .. import models, schemas
from .decorators import rollback_on_exception


def safe_file_name(s: str) -> str:
    s = normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = sub(r"[^\w\s-]", "", s).strip().lower()
    s = sub(r"[-\s]+", "_", s)
    return s


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
        db.query(models.ScenarioModel)
        .filter(models.ScenarioModel.name == scenario)
        .first()
    )
    run = sceanrio_model.run
    if run.version != version:
        run = None
        # Adding data to an older version
        for r in sceanrio_model.all_runs:
            if r.version == version:
                run = r
                break
        if run is None:  # Couldn't find version
            raise ValueError(f"couldn't find run with {version=} for {scenario=}")
    # Check if run has a DSS yet
    dss = run.dss
    if dss is None:
        s = safe_file_name(sceanrio_model.name)
        r = safe_file_name(run.version)
        dss = f"{s}_{r}.dss"
        run.dss = dss
    # Get the path model
    dsp = pdss.DatasetPath.from_str(path)
    path_str = f"/CALSIM/{dsp.b}/{dsp.c}//{dsp.e}/SERVER/"
    path_model = (
        db.query(models.NamedPathModel)
        .filter(models.NamedPathModel.path == path_str)
        .first()
    )
    if path_model is None:
        raise ValueError(
            "couldn't find the path for the given timeseries in the known "
            + "list, add the path and it's metadata first."
        )
    # Add the timeseries to the common catalog
    catalog_row = models.CommonCatalog(dss=dss, path_id=path_model.id)
    db.add(catalog_row)
    # Put the data into the DSS
    rts = pdss.RegularTimeseries.from_json(
        dict(
            path=path_str,  # TODO: update pandss to handle types better on from_json
            values=values,
            dates=dates,
            period_type=period_type,
            units=units,
            interval=interval,
        )
    )
    dss_obj = pdss.DSS(dss)
    with dss_obj:
        dss_obj.write_rts(path_str, rts)

    timeseries = schemas.Timeseries(scenario=scenario, version=version, **rts.to_json())

    db.commit()

    return timeseries


@rollback_on_exception
def read(
    db: Session,
    scenario: str = None,
    version: str = None,
    path: str = None,
) -> schemas.Timeseries:
    # Get the scenario, and the run we are adding data to
    sceanrio_model = (
        db.query(models.ScenarioModel)
        .filter(models.ScenarioModel.name == scenario)
        .first()
    )
    run = sceanrio_model.run
    if run.version != version:
        run = None
        # Adding data to an older version
        for r in sceanrio_model.all_runs:
            if r.version == version:
                run = r
                break
        if run is None:  # Couldn't find version
            raise ValueError(f"couldn't find run with {version=} for {scenario=}")
    # Check if run has a DSS yet
    dss = run.dss
    if not dss:
        raise ValueError("No data has been added to run yet")
    dsp = pdss.DatasetPath.from_str(path)
    path_str = f"/CALSIM/{dsp.b}/{dsp.c}//{dsp.e}/SERVER/"
    with pdss.DSS(dss) as dss_obj:
        rts = dss_obj.read_rts(path_str)

    return schemas.Timeseries(scenario=scenario, version=version, **rts.to_json())


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
