from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models import NamedPathModel, RunModel
from ..schemas import Timeseries

router = APIRouter(prefix="/timeseries", tags=["Timeseries"])


@router.get("", response_model=list[Timeseries])
async def get_timeseries(
    run_id: int = None,
    path_id: int = None,
    category: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"{run_id=}, {path_id=}, {category=}")

    return None
