from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models import TimestepModel
from ..schemas import Timestep

router = APIRouter(prefix="/timesteps", tags=["Timesteps"])


@router.get("", response_model=list[Timestep])
async def get_timesteps(db: Session = Depends(get_db)):
    logger.info("getting all runs")
    time_steps = db.query(TimestepModel).all()
    if time_steps is None:
        raise HTTPException(status_code=404, detail="Runs not found")

    logger.info(f"{len(time_steps)=}")

    return time_steps


@router.put("", response_model=Timestep)
async def put_timesteps(
    time_step: Timestep,
    db: Session = Depends(get_db),
):
    logger.info(f"{time_step=}")
    try:
        time_step = TimestepModel(**time_step.model_dump())
        db.add(time_step)
        db.commit()
        db.refresh(time_step)
    except HTTPException as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise e

    return time_step
