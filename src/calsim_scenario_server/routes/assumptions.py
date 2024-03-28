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


class AssumptionTable:
    name: str
    detail: str


assumption_tables: dict[str, AssumptionTable] = {
    "hydrology": AssumptionHydrology,
    "sea_level_rise": AssumptionSeaLevelRise,
    "land_use": AssumptionLandUse,
    "tucp": AssumptionTUCP,
    "dcp": AssumptionDeltaConveyanceProject,
    "va": AssumptionVoluntaryAgreements,
    "south_of_delta": AssumptionSouthOfDeltaStorage,
}


@router.get("/", response_model=dict[str, AssumptionIn])
async def get_assumption_types():
    logger.info("reporting schemas for assumption tables")
    schemas = dict()
    for table_name, model in assumption_tables.items():
        add_meta = {
            c.name: c.type.python_type.__name__
            for c in model.__table__.columns
            if c.name not in ("name", "detail", "id")
        }
        schemas[table_name] = {
            "name": "str",
            "detail": "str",
            "additional_metadata": add_meta,
        }
    return schemas


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
    logger.debug(assumptions)
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
        assumpt_in_db = db.query(tbl.id).filter(tbl.detail == assumption.detail).first()
        if assumpt_in_db is not None:
            logger.info("assumption already exists")
        else:
            kwargs = assumption.additional_metadata
            logger.info(f"detail={assumption.detail}, {kwargs=}")
            assumpt_in_db = tbl(detail=assumption.detail, **kwargs)
            db.add(assumpt_in_db)
            db.commit()
            db.refresh(assumpt_in_db)

    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    json_assumpt = assumption.model_dump()
    json_assumpt["id"] = assumpt_in_db.id
    return json_assumpt
