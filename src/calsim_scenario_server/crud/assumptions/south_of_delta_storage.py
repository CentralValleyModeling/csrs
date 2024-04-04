from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...models import AssumptionSouthOfDeltaStorage


def create(
    name: str,
    detail: str,
    db: Session,
) -> AssumptionSouthOfDeltaStorage:
    # check if it exists already
    dup_name = (
        db.query(AssumptionSouthOfDeltaStorage).filter_by(name=name).first() is not None
    )
    dup_detail = (
        db.query(AssumptionSouthOfDeltaStorage).filter_by(detail=detail).first()
        is not None
    )
    if dup_name or dup_detail:
        raise HTTPException(
            status_code=400,
            detail=f"assumption given is a duplicate, {dup_name=}, {dup_detail=}.",
        )
    model = AssumptionSouthOfDeltaStorage(name=name, detail=detail)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[AssumptionSouthOfDeltaStorage]:
    filters = list()
    if name:
        filters.append(AssumptionSouthOfDeltaStorage.name == name)
    if id:
        filters.append(AssumptionSouthOfDeltaStorage.id == id)
    return db.query(AssumptionSouthOfDeltaStorage).filter(*filters).all()


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
