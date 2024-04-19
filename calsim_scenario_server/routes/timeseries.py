from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..logger import logger

router = APIRouter(prefix="/timeseries", tags=["Timeseries"])


@router.get("", response_model=list[schemas.Timeseries])
async def get_timeseries(
    run_id: int = None,
    path_id: int = None,
    category: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"{run_id=}, {path_id=}, {category=}")

    return None


@router.put("", response_model=schemas.Timeseries)
async def put_timeseries(
    _in: schemas.Timeseries,
    db: Session = Depends(get_db),
):
    logger.info(_in)
    _out = crud.timeseries.create(db=db, **_in.model_dump())
    logger.debug(f"new timeseries {_out.path=}")
    return _out
