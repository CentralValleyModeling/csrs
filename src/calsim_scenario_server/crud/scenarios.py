from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import ScenarioModel
from ..schemas import Scenario
from . import assumptions


def validate_full_assumption_specification(assumptions_used: dict):
    missing = list()
    for attr in Scenario.model_fields:
        if attr not in assumptions_used:
            missing.append(attr)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"the scenario is missing assumptions:\n{missing}",
        )


def create(db: Session, name: str, **kwargs: dict[str, str]) -> ScenarioModel:
    validate_full_assumption_specification(kwargs)
    dup_name = db.query(ScenarioModel).filter_by(name=name).first() is not None
    if dup_name:
        raise HTTPException(status_code=400, detail=f"{name=} is already used")
    kwargs = dict()
    for table_name in Scenario.model_fields:
        assumption = kwargs[table_name]
        assumption_model = assumptions.read(db, id=assumption.id)
        if len(assumption_model) != 1:
            raise HTTPException(
                status_code=400,
                detail="couldn't find single assumption with data given:\n"
                + f"\tfound: {assumption_model}"
                + f"\tdetails given: {assumption}",
            )
        kwargs[table_name] = assumption_model[0].id
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
