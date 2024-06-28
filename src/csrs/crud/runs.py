from sqlalchemy.orm import Session

from .. import models, schemas
from ..errors import LookupUniqueError
from ..logger import logger
from ._common import common_update, rollback_on_exception
from .scenarios import read as read_scenario
from .scenarios import update as update_scenario


@rollback_on_exception
def model_to_schema(run: models.Run) -> schemas.Run:
    if run.parent:
        parent = run.parent.version
    else:
        parent = None
    if run.children:
        children = tuple(c.version for c in run.children)
    else:
        children = tuple()
    return schemas.Run(
        id=run.id,
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
    children: tuple[str, ...] = None,  # Will be ignored
    prefer_this_version: bool = True,
) -> schemas.Run:
    logger.info(f"creating new run for {scenario=}, {version=} {prefer_this_version=}")
    # get the information about the parents that we will need
    if parent:
        parent_lookup: list[schemas.Run] = read(db, scenario=scenario, version=parent)
        if len(parent_lookup) > 1:
            raise AttributeError("multiple potential predecessors found")
        if len(parent_lookup) == 0:
            raise AttributeError("no potential predecessors found")
        parent_id = parent_lookup[0].id
    else:
        parent_id = None
    if children:
        logger.warning(f"children specified, ignored in crud: {children=}")
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
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    # Add the run to the history table
    create_run_history(db, run.scenario_id, run.id, version)
    db.refresh(run)
    if prefer_this_version and version:
        update_scenario(db, id=scenario_model.id, preferred_run=version)
    db.refresh(run)

    return model_to_schema(run)


@rollback_on_exception
def create_run_history(
    db: Session,
    scenario_id: int,
    run_id: int,
    version: str,
) -> models.RunHistory:
    logger.info(f"creating run history {scenario_id=} {version=} {run_id=}")
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
    logger.info(
        f"reading new run where {scenario=} {version=} {code_version=} {contact=} {id=}"
    )
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


@rollback_on_exception
def update(
    db: Session,
    id: int,
    version: str | None = None,
    contact: str | None = None,
    confidential: bool | None = None,
    published: bool | None = None,
    code_version: str | None = None,
    detail: str | None = None,
) -> schemas.Run:
    logger.info(f"updating run where {id=}")
    obj = db.query(models.Run).where(models.Run.id == id).first()
    if not obj:
        raise LookupUniqueError(models.Run, obj, id=id)
    # All supported updates on Run are simple setattr actions,
    # so we will just use the common_update func using args that were not None
    updates = dict(  # make sure this dict uses all the args above
        version=version,
        contact=contact,
        confidential=confidential,
        published=published,
        code_version=code_version,
        detail=detail,
    )
    updates = {k: v for k, v in updates.items() if v is not None}
    logger.info(f"updating with {updates=}")
    obj = common_update(db, obj, **updates)
    db.commit()
    db.refresh(obj)
    return model_to_schema(obj)


def delete(
    db: Session,
    id: int,
) -> None:
    logger.info(f"deleteing run where {id=}")
    obj = db.query(models.Run).filter(models.Run.id == id).first()
    if not obj:
        raise ValueError(f"Cannot find Run with {id=}")
    db.query(models.Run).filter(models.Run.id == id).delete()
    db.commit()
