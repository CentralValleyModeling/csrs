from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Scenario
from ..schemas import ScenarioIn
from .assumptions import TableNames

SCENARIO_ATTR_TO_TABLE_NAME = (
    ("land_use_id", "land_use"),
    ("sea_level_rise_id", "sea_level_rise"),
    ("hydrology_id", "hydrology"),
    ("tucp_id", "tucp"),
    ("dcp_id", "dcp"),
    ("va_id", "va"),
    ("south_of_delta_id", "sod"),
)


def validate_full_assumption_specification(assumptions_used: dict):
    missing = list()
    for _, table_name in SCENARIO_ATTR_TO_TABLE_NAME:
        if table_name not in assumptions_used:
            missing.append(table_name)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"the scenario is missing assumptions:\n{missing}",
        )


def create(
    db: Session,
    name: str,
    assumptions_used: dict[str, ScenarioIn],
) -> Scenario:
    validate_full_assumption_specification(assumptions_used)
    dup_name = db.query(Scenario).filter_by(name=name).first() is not None
    if dup_name:
        raise HTTPException(status_code=400, detail=f"{name=} is already used")
    kwargs = dict()
    for attr_name, table_name in SCENARIO_ATTR_TO_TABLE_NAME:
        crud_module = TableNames[table_name].value
        assumption = assumptions_used[table_name]
        assumption_model = crud_module.read(db, id=assumption.id)
        if len(assumption_model) != 1:
            raise HTTPException(
                status_code=400,
                detail="couldn't find single assumption with data given:\n"
                + f"\tfound: {assumption_model}"
                + f"\tdetails given: {assumption}",
            )
        kwargs[attr_name] = assumption_model[0].id
    kwargs["name"] = name
    model = Scenario(**kwargs)
    db.add(model)
    db.commit()
    db.refresh(model)

    return model


def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[Scenario]:
    filters = list()
    if name:
        filters.append(Scenario.name == name)
    if id:
        filters.append(Scenario.id == id)
    return db.query(Scenario).filter(*filters).all()


def update() -> Scenario:
    raise NotImplementedError()


def delete() -> None:
    raise NotImplementedError()
