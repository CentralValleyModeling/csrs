from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models import NamedPathModel, RunModel, TimeseriesValueModel, TimestepModel
from ..schemas import TimeSeriesIn, TimeSeriesOut

router = APIRouter(prefix="/timeseries", tags=["Timeseries"])


@router.get("", response_model=list[TimeSeriesOut])
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
            filters.append(RunModel.id == run_id)
        if path_id is not None:
            filters.append(NamedPathModel.id == path_id)
        if category is not None:
            filters.append(NamedPathModel.category == category)
        if len(filters) == 0:
            raise HTTPException(
                status_code=413,
                detail="Requesting timeseries with no filters returns too much data.",
            )
        timeseries = (
            db.query(TimeseriesValueModel)
            .filter(*filters)
            .join(TimestepModel, TimestepModel.id == TimeseriesValueModel.timestep_id)
            .all()
        )
        logger.debug(f"returning {len(timeseries)} rows")

    except HTTPException as e:
        logger.error(f"HTTPException<{e.status_code}> {e.detail}")
        db.rollback()
        raise e

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return timeseries


@router.put("", response_model=TimeSeriesOut)
async def put_timeseries(
    ts_block: TimeSeriesIn,
    db: Session = Depends(get_db),
):
    logger.info(f"adding {ts_block.count} rows")
    try:
        ts_model = (
            TimeseriesValueModel(
                run_id=ts_block.run_ids[i],
                path_id=ts_block.path_ids[i],
                timestep_id=ts_block.timestep_ids[i],
                value=ts_block.values[i],
            )
            for i in range(ts_block.count)
        )
        # Add the new path to the database session
        db.add_all(ts_model)
        db.commit()
        db.refresh(ts_model)
    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return ts_model
