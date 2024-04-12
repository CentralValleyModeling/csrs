from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..logger import logger
from ..models import AssumptionModel


def create(
    name: str,
    kind: str,
    detail: str,
    db: Session,
) -> AssumptionModel:
    # check if it exists already
    dup_name = (
        db.query(AssumptionModel).filter_by(name=name, kind=kind).first() is not None
    )
    dup_detail = (
        db.query(AssumptionModel).filter_by(detail=detail, kind=kind).first()
        is not None
    )
    if dup_name or dup_detail:
        logger.error(f"error adding assumption, {dup_name=}, {dup_detail=}")
        raise HTTPException(
            status_code=400,
            detail=f"assumption given is a duplicate, {dup_name=}, {dup_detail=}.",
        )
    model = AssumptionModel(name=name, kind=kind, detail=detail)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def read(
    db: Session,
    kind: str = None,
    name: str = None,
    id: int = None,
) -> list[AssumptionModel]:
    logger.debug(f"reading assumptions where {kind=}, {name=}, {id=}")
    filters = list()
    if name:
        filters.append(AssumptionModel.name == name)
    if id:
        filters.append(AssumptionModel.id == id)
    if kind:
        filters.append(AssumptionModel.kind == kind)
    return db.query(AssumptionModel).filter(*filters).all()


def update() -> AssumptionModel:
    raise NotImplementedError()


def delete() -> None:
    raise NotImplementedError()
