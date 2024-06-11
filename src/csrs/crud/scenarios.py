from sqlalchemy.orm import Session

from .. import models, schemas
from ..errors import DuplicateScenarioError, LookupUniqueError
from ..logger import logger
from . import assumptions as assumptions_module
from ._common import rollback_on_exception


def model_to_schema(scenario: models.Scenario):
    kwargs = dict(
        name=scenario.name,
        id=scenario.id,
        version=scenario.version,
    )
    assumptions = dict()
    for mapping in scenario.assumption_maps:
        assumptions[mapping.assumption_kind] = mapping.assumption.name
    kwargs["assumptions"] = assumptions
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


@rollback_on_exception
def update_version(db: Session, name: str, new_version: str) -> schemas.Scenario:
    logger.info(f"updating {name} version to {new_version}")
    # Check to see if a run exists for the version, scenario
    scenario = db.query(models.Scenario).filter(models.Scenario.name == name).first()
    if scenario is None:
        raise LookupUniqueError(models.Scenario, scenario, name=name)
    # Check that run exists with that version
    runs = db.query(models.Run).filter(models.Run.scenario_id == scenario.id).all()
    runs = [r for r in runs if r.version == new_version]
    if len(runs) != 1:
        raise LookupUniqueError(models.Run, runs, version=new_version)
    run = runs[0]
    # Change preference
    update_preference(db, scenario.id, run.id)
    db.refresh(scenario)
    logger.debug(f"{scenario.name} version is now {scenario.version}")

    return model_to_schema(scenario)


@rollback_on_exception
def update_preference(
    db: Session,
    scenario_id: int,
    run_id: int,
) -> models.PreferredVersion:
    pref = (
        db.query(models.PreferredVersion)
        .filter(models.PreferredVersion.scenario_id == scenario_id)
        .first()
    )
    if pref is None:
        pref = models.PreferredVersion(scenario_id=scenario_id, run_id=run_id)
        db.add(pref)
    else:
        pref.run_id = run_id
    db.commit()
    db.refresh(pref)

    return pref


def delete() -> None:
    raise NotImplementedError()