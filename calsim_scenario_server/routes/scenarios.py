from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.http.scenarios import ScenarioIdMetadata
from ..models.sql import Scenario

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])


@router.get("/")
async def get_names(db: Session = Depends(get_db)):
    scenarios = db.query(Scenario).all()
    if scenarios is None:
        raise HTTPException(status_code=404, detail="No scenarios found")
    return [{"id": s.id, "scenario_name": s.scenario_name} for s in scenarios]


@router.get("/{scenario_id}")
async def get_one_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="No scenarios found")
    return scenario


@router.put("/")
async def put_scenario(
    scenario: ScenarioIdMetadata,
    db: Session = Depends(get_db),
):
    try:
        new = Scenario(**scenario.model_dump())
        db.add(new)
        db.commit()
        db.refresh(new)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return new
