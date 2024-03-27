from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models import (
    AssumptionDeltaConveyanceProject,
    AssumptionHydrology,
    AssumptionLandUse,
    AssumptionSeaLevelRise,
    AssumptionSouthOfDeltaStorage,
    AssumptionTUCP,
    AssumptionVoluntaryAgreements,
)
from ..schemas import AssumptionIn, AssumptionOut

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


@router.get("/", response_model=list[AssumptionOut])
async def get_size_of_assumption_tables(db: Session = Depends(get_db)):
    logger.info("getting the shape of assumption tables")
    assumption_count = [
        {
            "name": k,
            "rows": db.query(assumption_tables[k]).count(),
            "column_names": [c.name for c in assumption_tables[k].__table__.columns],
        }
        for k in assumption_tables
    ]

    return assumption_count


@router.get("/{assumption_type}")
async def get_assumption(assumption_type: str, db: Session = Depends(get_db)):
    logger.info(f"{assumption_type=}")
    if assumption_type not in assumption_tables:
        raise HTTPException(status_code=404, detail="Assumption table not in schema")
    tbl = assumption_tables[assumption_type]
    assumptions = db.query(tbl).all()

    if assumptions is None:
        logger.error(f"no table found for {assumption_type=}")
        raise HTTPException(status_code=404, detail="No assumptions in table")

    return [a for a in assumptions]


@router.put("/{assumption_type}", response_model=AssumptionOut)
async def put_assumption(
    assumption_type: str,
    assumption: AssumptionIn,
    db: Session = Depends(get_db),
):
    logger.info(f"{assumption_type=}, {assumption=}")
    if assumption_type not in assumption_tables:
        raise HTTPException(status_code=404, detail="Assumption table not in schema")
    try:
        tbl = assumption_tables[assumption_type]
        kwargs = assumption.additional_fields
        logger.info(f"detail={assumption.detail}, {kwargs=}")
        new_assumption = tbl(detail=assumption.detail, **kwargs)
        db.add(new_assumption)
        db.commit()
        db.refresh(new_assumption)

    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    return new_assumption
