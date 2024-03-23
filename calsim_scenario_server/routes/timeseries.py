from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..logger import logger
from ..models import Path, Run, TimeSeriesValue, TimeStep
from . import get_db

router = APIRouter(prefix="/timeseries")


class TimeSeriesValueModel(BaseModel):
    run_id: int
    path_id: int
    timestep_id: int
    value: float


class TimeSeriesBlockModel(BaseModel):
    data: list[TimeSeriesValueModel]


@router.get("/", response_model=list[TimeSeriesValueModel])
async def get_timeseries(
    run_id: int = None,
    path_id: int = None,
    category: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"{run_id=}, {path_id=}, {category=}")
    try:
        filters = list()
        if run_id is not None:
            filters.append(Run.id == run_id)
        if path_id is not None:
            filters.append(Path.id == path_id)
        if category is not None:
            filters.append(Path.category == category)
        if len(filters) == 0:
            raise HTTPException(
                status_code=413,
                detail="Requesting timeseries with no filters returns too much data.",
            )
        timeseries = (
            db.query(TimeSeriesValue)
            .filter(*filters)
            .join(TimeStep, TimeStep.id == TimeSeriesValue.timestep_id)
            .all()
        )
        logger.info(f"returning {len(timeseries)} rows")

        return timeseries
    except HTTPException as e:
        logger.error(f"HTTPException<{e.status_code}> {e.detail}")
        db.rollback()
        raise e
    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=TimeSeriesBlockModel)
async def post_timeseries(
    ts_block: TimeSeriesBlockModel,
    db: Session = Depends(get_db),
):
    logger.info(f"adding {len(ts_block.data)} rows")
    try:
        ts_model = [TimeSeriesValue(**ts.model_dump()) for ts in ts_block.data]
        # Add the new path to the database session
        db.add_all(ts_model)
        db.commit()
        db.refresh(ts_model)
        return ts_block
    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
