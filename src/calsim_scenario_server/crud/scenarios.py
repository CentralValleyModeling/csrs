from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..logger import logger
from ..models import ScenarioModel
from ..schemas import Scenario
from . import assumptions


def validate_full_assumption_specification(assumptions_used: dict):
    missing = list()
    for attr in Scenario.get_assumption_names():
        if attr not in assumptions_used:
            missing.append(attr)
    if missing:
        logger.error(f"missing scenario assumptions: {missing}")
        raise HTTPException(
            status_code=400,
            detail=f"the scenario is missing assumptions:\n{missing}",
        )


def create(db: Session, name: str, **kwargs: dict[str, str]) -> ScenarioModel:
    logger.info(f"adding scenario, {name=}")
    validate_full_assumption_specification(kwargs)
    dup_name = db.query(ScenarioModel).filter_by(name=name).first() is not None
    if dup_name:
        logger.error(f"{dup_name=}")
        raise HTTPException(status_code=400, detail=f"{name=} is already used")
    for table_name in Scenario.get_assumption_names():
        assumption_model = assumptions.read(
            db,
            kind=table_name,
            name=kwargs[table_name],
        )
        if len(assumption_model) != 1:
            logger.error("more than one assumption corresponds")
            raise HTTPException(
                status_code=400,
                detail="couldn't find single assumption with data given:\n"
                + f"\tfound: {assumption_model}"
                + f"\tdetails given: {kwargs[table_name]}",
            )
        kwargs[table_name] = assumption_model[0].name
    kwargs["name"] = name
    model = ScenarioModel(**kwargs)
    db.add(model)
    db.commit()
    db.refresh(model)

    return model


def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[ScenarioModel]:
    filters = list()
    if name:
        filters.append(ScenarioModel.name == name)
    if id:
        filters.append(ScenarioModel.id == id)
    return db.query(ScenarioModel).filter(*filters).all()


def update() -> ScenarioModel:
    raise NotImplementedError()


def delete() -> None:
    raise NotImplementedError()
