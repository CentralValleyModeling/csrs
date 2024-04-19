from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..logger import logger

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


@router.get("", response_model=list[schemas.Scenario])
async def get_scenario(
    name: str = None,
    id: int = None,
    db: Session = Depends(get_db),
):
    logger.info(f"getting scenarios, filtered where {name=}, {id=}")
    scenarios = crud.scenarios.read(db, name=name, id=id)
    logger.debug(f"{len(scenarios)} scenarios found")
    for s in scenarios:
        logger.debug(f"{s.name=}")
    return scenarios


@router.put("/", response_model=schemas.Scenario)
async def put_scenario(
    _in: schemas.Scenario,
    db: Session = Depends(get_db),
):
    logger.info(_in)
    _out = crud.scenarios.create(db=db, **_in.model_dump(exclude=("id")))
    logger.debug(f"new scenario {_out.id=}")
    return _out
