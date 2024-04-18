from sqlalchemy.orm import Session

from .. import models, schemas
from ..logger import logger
from .decorators import rollback_on_exception
from .scenarios import read as read_scenario
from .scenarios import update_version


@rollback_on_exception
def model_to_schema(run: models.Run) -> schemas.Run:
    if run.parent:
        parent = run.parent.history
    else:
        parent = None
    if run.children:
        children = tuple(c.history for c in run.children)
    else:
        children = tuple()
    return schemas.Run(
        scenario=run.scenario.name,
        version=run.version,
        # info
        parent=parent,
        children=children,
        contact=run.contact,
        confidential=run.confidential,
        published=run.published,
        code_version=run.code_version,
        detail=run.detail,
    )


@rollback_on_exception
def create(
    db: Session,
    scenario: str,
    version: str,
    contact: str,
    code_version: str,
    detail: str,
    published: bool = False,
    confidential: bool = True,
    parent: str = None,
    dss: str = None,
    prefer_this_version: bool = True,
) -> schemas.Run:
    logger.info(f"creating new run for {scenario=}, {version=} {prefer_this_version=}")
    # get the information about the parents that we will need
    if parent:
        parent: list[schemas.Run] = read(db, scenario=scenario, version=parent)
        if len(parent) != 1:
            raise AttributeError("multiple potential predecessors found")
        parent_id = parent[0].id
    else:
        parent_id = None
    # Get the scenario
    (scenario_model,) = read_scenario(db=db, name=scenario)
    # Create the run model
    run = models.Run(
        scenario_id=scenario_model.id,
        parent_id=parent_id,
        contact=contact,
        code_version=code_version,
        detail=detail,
        published=published,
        confidential=confidential,
        dss=dss,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    # Add the run to the history table
    create_run_history(db, run.scenario_id, run.id, version)
    db.refresh(run)
    if prefer_this_version:
        update_version(db, scenario, version)
    db.refresh(run)

    return model_to_schema(run)


@rollback_on_exception
def create_run_history(
    db: Session,
    scenario_id: int,
    run_id: int,
    version: str,
) -> models.RunHistory:
    hist = models.RunHistory(scenario_id=scenario_id, run_id=run_id, version=version)
    db.add(hist)
    db.commit()
    db.refresh(hist)

    return hist


def read(
    db: Session,
    scenario: str = None,
    version: str = None,
    code_version: str = None,
    contact: str = None,
    id: int = None,
) -> list[schemas.Run]:
    filters = list()
    if scenario:
        (scenario_obj,) = read_scenario(db, name=scenario)
        filters.append(models.Run.scenario_id == scenario_obj.id)
    if code_version:
        filters.append(models.Run.code_version == code_version)
    if id:
        filters.append(models.Run.id == id)
    if contact:
        filters.append(models.Run.contact == contact)
    runs = db.query(models.Run).filter(*filters).all()
    if version:
        runs = [r for r in runs if r.version == version]
    return [model_to_schema(r) for r in runs]


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
