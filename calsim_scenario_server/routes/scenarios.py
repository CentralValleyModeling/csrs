from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..logger import logger
from ..models import ScenarioModel
from ..schemas import Scenario

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


def build_response_from_model(db: Session, model: ScenarioModel) -> Scenario:
    kwargs = dict()
    for attr in Scenario.get_assumption_names():
        name = getattr(model, attr)
        kwargs[attr] = name
    logger.info(f"{kwargs=}")
    return Scenario(id=model.id, name=model.name, **kwargs)


@router.get("", response_model=list[Scenario])
async def get_scenario(
    name: str = None,
    id: int = None,
    db: Session = Depends(get_db),
):
    logger.info(f"getting scenarios, filtered where {name=}, {id=}")
    models = crud.scenarios.read(db, name=name, id=id)
    logger.debug(f"{len(models)} scenarios found")
    for m in models:
        logger.debug(f"{m.name=}")
    return [build_response_from_model(db, m) for m in models]


@router.put("", response_model=Scenario)
async def put_scenario(
    scenario: Scenario,
    db: Session = Depends(get_db),
):
    logger.info(f"{scenario.name=}")
    model = crud.scenarios.create(db, **scenario.model_dump(exclude=("id")))
    return build_response_from_model(db, model)
