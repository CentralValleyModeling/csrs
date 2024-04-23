from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..logger import logger

router = APIRouter(prefix="/runs", tags=["Model Runs"])


@router.get("", response_model=list[schemas.Run])
async def get_runs(
    scenario: str = None,
    version: str = None,
    code_version: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"getting all runs, filters, {scenario=}, {version=}, {code_version=}")
    runs = crud.runs.read(
        db=db,
        scenario=scenario,
        version=version,
        code_version=code_version,
    )
    logger.info(f"runs: {[(r.scenario, r.version) for r in runs]}")

    return runs


@router.put("", response_model=schemas.Run)
async def put_run(
    _in: schemas.Run,
    db: Session = Depends(get_db),
):
    logger.info(_in)
    _out = crud.runs.create(
        db=db,
        prefer_this_version=True,  # Prefer this new run on the scenario
        **_in.model_dump(exclude=("id")),
    )
    logger.debug(f"new run {_out.id=}")
    return _out


@router.put("/legacy", response_model=schemas.Run)
async def put_legacy_run(
    _in: schemas.Run,
    db: Session = Depends(get_db),
):
    logger.info(_in)
    _out = crud.runs.create(
        db=db,
        prefer_this_version=False,  # Do not change the preferred run for scenario
        **_in.model_dump(exclude=("id")),
    )
    logger.debug(f"new run {_out.id=}")
    return _out
