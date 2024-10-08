import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/assumptions", tags=["Assumptions"])
logger = logging.getLogger(__name__)


@router.get("/names", response_model=tuple[str, ...])
async def get_assumption_table_names(db: Session = Depends(get_db)):
    logger.info("getting assumption categories")
    return crud.assumptions.read_kinds(db=db)


@router.get("", response_model=list[schemas.Assumption])
async def get_assumption(
    id: int = None,
    name: str = None,
    kind: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"{id=}, {name=}, {kind=}")
    models = crud.assumptions.read(db=db, id=id, name=name, kind=kind)
    logger.debug(f"{len(models)} assumptions found")
    for m in models:
        logger.debug(f"{m.name=}, {m.detail=}")
    return models


@router.put("", response_model=schemas.Assumption)
async def put_assumption(
    _in: schemas.Assumption,
    db: Session = Depends(get_db),
):
    logger.info(_in)
    _out = crud.assumptions.create(db=db, **_in.model_dump(exclude=("id")))
    logger.debug(f"new assumption {_out.id=}")
    return _out
