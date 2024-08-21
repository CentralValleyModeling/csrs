import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..errors import UniqueLookupError

router = APIRouter(prefix="/timeseries", tags=["Timeseries"])
logger = logging.getLogger(__name__)


@router.get("", response_model=schemas.Timeseries)
async def get_timeseries(
    scenario: str = None,
    version: str = None,
    path: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"getting all timeseries, filters, {scenario=}, {version=}, {path=}")
    try:
        ts = crud.timeseries.read(
            db=db,
            scenario=scenario,
            version=version,
            path=path,
        )
    except UniqueLookupError:
        raise HTTPException(
            status_code=404,
            detail=f"couldn't find unique {path=} in database",
        )
    logger.info(f"timeseries: {ts.scenario}, {ts.version}, {ts.path}")
    return ts


@router.put("", response_model=schemas.Timeseries)
async def put_timeseries(
    _in: schemas.Timeseries,
    db: Session = Depends(get_db),
):
    logger.info(_in)
    _out = crud.timeseries.create(
        db=db,
        **_in.model_dump(exclude=("id")),
    )
    logger.debug(f"new timeseries {_out.scenario}, {_out.version}, {_out.path}")
    return _out
