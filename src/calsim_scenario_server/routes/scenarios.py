from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..logger import logger
from ..models import Scenario
from ..schemas import ScenarioIn, ScenarioOut
from .assumptions import (
    build_reposne_from_model as build_assumption_response_from_model,
)

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


def build_response_from_model(db: Session, model: Scenario) -> ScenarioOut:
    assumptions = dict()
    for attr, table_name in crud.scenarios.SCENARIO_ATTR_TO_TABLE_NAME:
        id = getattr(model, attr)
        reader = crud.assumptions.TableNames[table_name].value
        assumpt_models = reader.read(db, id=id)
        if len(assumpt_models) != 1:
            raise HTTPException(
                status_code=400,
                detail="couldn't find single assumption with data given:\n"
                + f"\tfound: {assumpt_models}"
                + f"\tdetails given: {id=}",
            )
        assumptions[attr] = build_assumption_response_from_model(
            assumpt_models[0]
        ).model_dump()

    logger.info(f"{assumptions=}")
    return ScenarioOut(id=model.id, name=model.name, assumptions_used=assumptions)


@router.get("", response_model=list[ScenarioOut])
async def get_scenario(
    name: str = None,
    id: int = None,
    db: Session = Depends(get_db),
):
    logger.info(f"getting scenarios, filtered where {name=}, {id=}")
    models = crud.scenarios.read(db, name=name, id=id)
    logger.info(f"{len(models)} scenarios found")
    for m in models:
        logger.debug(f"{m.name=}")
    return [build_response_from_model(db, m) for m in models]


@router.put("", response_model=ScenarioOut)
async def put_scenario(
    scenario: ScenarioIn,
    db: Session = Depends(get_db),
):
    logger.info(f"{scenario.name}, {scenario.assumptions_used=}")
    model = crud.scenarios.create(
        db,
        name=scenario.name,
        assumptions_used=scenario.assumptions_used,
    )
    return build_response_from_model(db, model)
