from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..logger import logger
from ..models import Scenario
from ..schemas import Run

router = APIRouter(prefix="/runs", tags=["Model Runs"])


def assert_scenario_exists(s_id: int | None, db: Session):
    if s_id is not None:
        s_count = db.query(Scenario).filter(Scenario.id == s_id).count()
        if s_count != 1:
            logger.error(f"scenario_id was not found, {s_id=}")
            raise HTTPException(
                status_code=400,
                detail=f"scenario_id={s_id} not found, you need to add it first",
            )


@router.get("", response_model=list[Run])
async def get_all_runs(
    id: int = None,
    name: str = None,
    db: Session = Depends(get_db),
):
    logger.info("getting all runs")
    runs = crud.runs.read(db, id=id, name=name)
    logger.info(f"{runs=}")

    return runs
