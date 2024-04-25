from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..logger import logger

router = APIRouter(prefix="/paths", tags=["Paths"])


@router.get("", response_model=list[schemas.NamedPath])
async def get_paths(
    name: str = None,
    path: str = None,
    category: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"getting all runs, filters, {name=}, {path=}, {category=}")
    paths = crud.paths.read(
        db=db,
        name=name,
        path=path,
        category=category,
    )
    logger.info(f"paths: {[(p.name, p.path) for p in paths]}")

    return paths


@router.put("", response_model=schemas.NamedPath)
async def put_path(
    _in: schemas.NamedPath,
    db: Session = Depends(get_db),
):
    logger.info(_in)
    _out = crud.paths.create(
        db=db,
        **_in.model_dump(exclude=("id")),
    )
    logger.debug(f"new path {_out.id=}")
    return _out
