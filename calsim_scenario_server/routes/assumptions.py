from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.http.assumptions import AssumptionDetails, AssumptionSummary
from ..models.sql import (
    AssumptionDeltaConveyanceProject,
    AssumptionHydrology,
    AssumptionLandUse,
    AssumptionSeaLevelRise,
    AssumptionSouthOfDeltaStorage,
    AssumptionTUCP,
    AssumptionVoluntaryAgreements,
)

router = APIRouter(prefix="/assumptions", tags=["Assumptions"])

assumption_tables = {
    "hydrology": AssumptionHydrology,
    "sea_level_rise": AssumptionSeaLevelRise,
    "land_use": AssumptionLandUse,
    "tucp": AssumptionTUCP,
    "dcp": AssumptionDeltaConveyanceProject,
    "va": AssumptionVoluntaryAgreements,
    "south_of_delta": AssumptionSouthOfDeltaStorage,
}


@router.get("/", response_model=list[AssumptionSummary])
async def get_size_of_assumption_tables(db: Session = Depends(get_db)):
    assumption_count = [
        {
            "name": k,
            "rows": db.query(assumption_tables[k]).count(),
            "column_names": [c.name for c in assumption_tables[k].__table__.columns],
        }
        for k in assumption_tables
    ]

    return assumption_count


@router.get("/{assumption_type}", response_model=list[AssumptionDetails])
async def get_assumption(assumption_type: str, db: Session = Depends(get_db)):

    if assumption_type not in assumption_tables:
        raise HTTPException(status_code=404, detail="Assumption table not in schema")
    tbl = assumption_tables[assumption_type]
    assumptions = db.query(tbl).all()

    if assumptions is None:
        raise HTTPException(status_code=404, detail="No assumptions in table")

    return [AssumptionDetails(a.detail) for a in assumptions]
