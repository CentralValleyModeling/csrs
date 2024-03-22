from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import Scenario
from . import get_db

router = APIRouter(prefix="/scenario")


@router.get("/scenarios/{scenario_id}")
async def get_names(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@router.get("/scenarios/{scenario_id}")
async def get_metadata(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@router.get("/scenarios/{scenario_id}")
async def get_timeseries(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario
