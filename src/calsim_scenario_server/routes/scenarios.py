from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models import Scenario
from ..schemas import ScenarioIn, ScenarioOut
from .assumptions import assumption_tables

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


@router.get("/", response_model=list[ScenarioOut])
async def get_names(db: Session = Depends(get_db)):
    logger.info("getting all scenarios metadata")
    scenarios = db.query(Scenario).all()
    if scenarios is None:
        logger.error("no scenarios found")
        raise HTTPException(status_code=404, detail="No scenarios found")
    logger.info(f"{len(scenarios)=}")
    return [s for s in scenarios]


@router.get("/{scenario_id}")
async def get_one_scenario(scenario_id: int, db: Session = Depends(get_db)):
    logger.info(f"getting one scenario: {scenario_id=}")
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        logger.error("no scenarios found")
        raise HTTPException(status_code=404, detail="No scenarios found")
    return scenario


@router.put("/", response_model=ScenarioOut)
async def put_scenario(
    scenario: ScenarioIn,
    db: Session = Depends(get_db),
):
    logger.info(f"{scenario=}")
    try:
        kwargs = {
            k: v
            for k, v in scenario.model_dump().items()
            if k not in ("assumptions_used")
        }
        # FIXME: The user gives the assumption objects
        new = Scenario(**kwargs)
        db.add(new)
        db.commit()
        db.refresh(new)

    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    return new
