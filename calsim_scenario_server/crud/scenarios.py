from sqlalchemy.orm import Session

from .. import models, schemas
from ..logger import logger
from . import assumptions
from .decorators import rollback_on_exception


def validate_full_assumption_specification(assumptions_used: dict):
    missing = list()
    for attr in schemas.Scenario.get_assumption_attrs():
        if attr not in assumptions_used:
            missing.append(attr)
    if missing:
        logger.error(f"missing scenario assumptions: {missing}")
        raise AttributeError(
            f"the scenario is missing assumptions:\n{missing}",
        )


def model_to_schema(scenario: models.Scenario):
    kwargs = dict(name=scenario.name, id=scenario.id)
    for mapping in scenario.assumption_maps:
        kwargs[mapping.assumption_kind] = mapping.assumption.name
    kwargs["version"] = scenario.version
    return schemas.Scenario(**kwargs)


@rollback_on_exception
def create(
    db: Session,
    name: str,
    **kwargs: dict[str, str],
) -> schemas.Scenario:
    logger.info(f"adding scenario, {name=}")
    validate_full_assumption_specification(kwargs)
    dup_name = db.query(models.Scenario).filter_by(name=name).first() is not None
    if dup_name:
        logger.error(f"{dup_name=}")
        raise AttributeError(f"{name=} is already used")
    scenario_assumptions = dict()
    for table_name in schemas.Scenario.get_assumption_attrs():
        assumption_model = assumptions.read(
            db,
            kind=table_name,
            name=kwargs[table_name],
        )
        if len(assumption_model) != 1:
            logger.error("more than one assumption corresponds")
            raise AttributeError(
                "couldn't find single assumption with data given:\n"
                + f"\tfound: {assumption_model}"
                + f"\tdetails given: {kwargs[table_name]}",
            )
        scenario_assumptions[table_name] = assumption_model[0].id
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
        raise ValueError(f"could not find scenario where {name=}")
    # Check that run exists with that version
    runs = db.query(models.Run).filter(models.Run.scenario_id == scenario.id).all()
    runs = [r for r in runs if r.version == new_version]
    if len(runs) != 1:
        raise ValueError(
            f"could not find unqiue run for scenario {name=}, {new_version=}"
        )
    run = runs[0]
    if run is None:
        raise ValueError("cannot set scenario version to a run that does not exist")
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
