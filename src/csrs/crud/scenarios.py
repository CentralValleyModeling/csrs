from sqlalchemy.orm import Session

from .. import models, schemas
from ..errors import DuplicateScenarioError, LookupUniqueError
from ..logger import logger
from . import assumptions as assumptions_module
from ._common import rollback_on_exception


def model_to_schema(scenario: models.Scenario):
    assumptions = dict()
    for mapping in scenario.assumption_maps:
        assumptions[mapping.assumption_kind] = mapping.assumption.name
    kwargs = dict(
        name=scenario.name,
        id=scenario.id,
        preferred_run=scenario.version,
        assumptions=assumptions,
    )
    return schemas.Scenario(**kwargs)


@rollback_on_exception
def create(
    db: Session,
    name: str,
    assumptions: dict[str, str],
    preferred_run: str | None = None,
) -> schemas.Scenario:
    logger.info(f"adding scenario, {name=}")
    if preferred_run:
        logger.info(
            "when creating a new `Scenario`, the `preferred_run` attr is ignored "
            + "until the corresponding `Run` is created."
        )
    dup_name = db.query(models.Scenario).filter_by(name=name).first() is not None
    if dup_name:
        logger.error(f"{dup_name=}")
        raise DuplicateScenarioError(name)
    scenario_assumptions = dict()
    for a_kind, a_name in assumptions.items():
        assumption_model = assumptions_module.read(db, kind=a_kind, name=a_name)
        if len(assumption_model) != 1:
            logger.error("more than one assumption corresponds")
            raise LookupUniqueError(
                models.Assumption,
                assumption_model,
                table_name=a_kind,
            )
        scenario_assumptions[a_kind] = assumption_model[0].id
    scenario_model = models.Scenario(name=name)
    # Update assumptions mapping
    db.add(scenario_model)
    db.flush()
    db.refresh(scenario_model)
    models_to_add = list()
    for kind, id in scenario_assumptions.items():
        models_to_add.append(
            models.ScenarioAssumptions(
                scenario_id=scenario_model.id,
                assumption_id=id,
                assumption_kind=kind,
            )
        )
    db.add_all(models_to_add)
    db.commit()
    db.refresh(scenario_model)

    return model_to_schema(scenario_model)


@rollback_on_exception
def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[schemas.Scenario]:
    filters = list()
    if name:
        filters.append(models.Scenario.name == name)
    if id:
        filters.append(models.Scenario.id == id)
    result = db.query(models.Scenario).filter(*filters).all()
    return [model_to_schema(mod) for mod in result]


def _update_name(
    db: Session,
    id: int,
    name: str,
) -> models.Scenario:
    obj = db.query(models.Scenario).filter(models.Scenario.id == id).first()
    obj.name = name
    db.commit()
    db.refresh(obj)
    return obj


def _update_preferred_run(db: Session, id: int, preferred_run: str) -> models.Scenario:
    # Retrieve the Run model from the database
    run = (
        db.query(models.Run)
        .join(models.RunHistory)
        .filter(models.RunHistory.scenario_id == id)
        .filter(models.RunHistory.version == preferred_run)
        .first()
    )
    if not run:  # Specied Run not found
        raise LookupUniqueError(
            models.Run,
            run,
            version=preferred_run,
            scenario_id=id,
        )
    # Find the PreferredVersion object in the db, this stores preferences
    pref = (
        db.query(models.PreferredVersion)
        .where(models.PreferredVersion.scenario_id == id)
        .first()
    )
    if pref is None:  # Newly created Scenario without a preferred Run set
        pref = models.PreferredVersion(scenario_id=id, run_id=run.id)
        db.add(pref)
    else:
        pref.run_id = run.id
    db.commit()
    return db.query(models.Scenario).filter(models.Scenario.id == id).first()


def _update_assumptions(
    db: Session,
    id: int,
    assumptions: dict[str, str],
) -> models.Scenario:
    # Depending if the assumptions given are replacing old, or are new specs...
    obj = db.query(models.Scenario).filter(models.Scenario.id == id).first()
    existing_assumption_kinds = [a.assumption_kind for a in obj.assumption_maps]
    for kind, name in assumptions.items():
        assumption_obj = assumptions_module.read(db, kind=kind, name=name)
        if len(assumption_obj) != 0:
            raise LookupUniqueError(
                models.Assumption,
                assumption_obj,
                kind=kind,
                name=name,
            )
        assumption_obj = assumption_obj[0]
        if assumption_obj.kind in existing_assumption_kinds:
            # Update the ScenarioAssumptions objects for these
            scenario_assumption_obj = (
                db.query(models.ScenarioAssumptions)
                .where(models.ScenarioAssumptions.scenario_id == id)
                .where(models.ScenarioAssumptions.assumption_kind == kind)
                .first()
            )
            scenario_assumption_obj.assumption_id = assumption_obj.id
        else:
            scenario_assumption_obj = models.ScenarioAssumptions(
                scenaio_id=id,
                assumption_id=assumption_obj.id,
                assumption_kind=assumption_obj.kind,
            )
            db.add(scenario_assumption_obj)
    db.commit()
    db.refresh(obj)
    return obj


@rollback_on_exception
def update(
    db: Session,
    id: int,
    name: str | None = None,
    preferred_run: str | None = None,
    assumptions: dict[str, str] = None,
) -> schemas.Scenario:
    obj = db.query(models.Scenario).filter(models.Scenario.id == id).first()
    if not obj:
        raise LookupUniqueError(models.Scenario, obj, id=id)
    if name:
        _update_name(db, id, name)
    if preferred_run:
        _update_preferred_run(db, id, preferred_run)
    if assumptions:
        _update_assumptions(db, id, assumptions)
    db.commit()
    db.refresh(obj)

    return model_to_schema(obj)


def delete() -> None:
    raise NotImplementedError()
