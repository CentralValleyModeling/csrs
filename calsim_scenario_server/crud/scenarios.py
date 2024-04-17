from sqlalchemy.orm import Session

from ..logger import logger
from ..models import ScenarioAssumptionsModel, ScenarioModel
from ..schemas import Scenario
from . import assumptions
from .decorators import rollback_on_exception


def validate_full_assumption_specification(assumptions_used: dict):
    missing = list()
    for attr in Scenario.get_assumption_names():
        if attr not in assumptions_used:
            missing.append(attr)
    if missing:
        logger.error(f"missing scenario assumptions: {missing}")
        raise AttributeError(
            f"the scenario is missing assumptions:\n{missing}",
        )


def model_to_schema(scenario: ScenarioModel):
    kwargs = dict(name=scenario.name, id=scenario.id)
    for mapping in scenario.assumption_maps:
        kwargs[mapping.assumption_kind] = mapping.assumption.name
    return Scenario(**kwargs)


@rollback_on_exception
def create(
    db: Session,
    name: str,
    version: str = None,
    **kwargs: dict[str, str],
) -> Scenario:
    logger.info(f"adding scenario, {name=}")
    validate_full_assumption_specification(kwargs)
    dup_name = db.query(ScenarioModel).filter_by(name=name).first() is not None
    if dup_name:
        logger.error(f"{dup_name=}")
        raise AttributeError(f"{name=} is already used")
    scenario_assumptions = dict()
    for table_name in Scenario.get_assumption_names():
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
    scenario_model = ScenarioModel(name=name, version=version)
    db.add(scenario_model)
    db.flush()
    db.refresh(scenario_model)
    models_to_add = list()
    for kind, id in scenario_assumptions.items():
        models_to_add.append(
            ScenarioAssumptionsModel(
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
) -> list[Scenario]:
    filters = list()
    if name:
        filters.append(ScenarioModel.name == name)
    if id:
        filters.append(ScenarioModel.id == id)
    result = db.query(ScenarioModel).filter(*filters).all()
    return [model_to_schema(m) for m in result]


def update_version(db: Session, name: str, new_version: str) -> ScenarioModel:
    db.query(ScenarioModel).filter(ScenarioModel.name == name).update(
        {ScenarioModel.version: new_version}
    )
    db.commit()


def delete() -> None:
    raise NotImplementedError()
