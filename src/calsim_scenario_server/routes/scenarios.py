from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..crud import assumptions
from ..database import get_db
from ..logger import logger
from ..models import ScenarioModel
from ..schemas import Scenario
from .assumptions import (
    build_reposne_from_model as build_assumption_response_from_model,
)

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


def build_response_from_model(db: Session, model: ScenarioModel) -> Scenario:
    assumptions_dict = dict()
    for attr, table_name in crud.scenarios.SCENARIO_ATTR_TO_TABLE_NAME:
        id = getattr(model, attr)
        assumpt_models = assumptions.read(db, id=id)
        if len(assumpt_models) != 1:
            raise HTTPException(
                status_code=400,
                detail="couldn't find single assumption with data given:\n"
                + f"\tfound: {assumpt_models}"
                + f"\tdetails given: {id=}",
            )
        assumptions_dict[attr] = build_assumption_response_from_model(
            assumpt_models[0]
        ).model_dump()

    logger.info(f"{assumptions_dict=}")
    return Scenario(id=model.id, name=model.name, assumptions_used=assumptions_dict)


@router.get("", response_model=list[Scenario])
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


@router.put("", response_model=Scenario)
async def put_scenario(
    scenario: Scenario,
    db: Session = Depends(get_db),
):
    logger.info(f"{scenario.name}")
    model = crud.scenarios.create(db, **scenario.model_dump(exclude=("id")))
    return build_response_from_model(db, model)
