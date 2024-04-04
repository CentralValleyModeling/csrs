from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...models import AssumptionLandUse


def create(
    name: str,
    detail: str,
    future_year: int,
    db: Session,
) -> AssumptionLandUse:
    # check if it exists already
    dup_name = db.query(AssumptionLandUse).filter_by(name=name).first() is not None
    dup_detail = (
        db.query(AssumptionLandUse).filter_by(detail=detail).first() is not None
    )
    if dup_name or dup_detail:
        raise HTTPException(
            status_code=400,
            detail=f"assumption given is a duplicate, {dup_name=}, {dup_detail=}.",
        )
    model = AssumptionLandUse(name=name, detail=detail, future_year=future_year)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def read(
    db: Session,
    name: str = None,
    id: int = None,
    future_year: int = None,
) -> list[AssumptionLandUse]:
    filters = list()
    if name:
        filters.append(AssumptionLandUse.name == name)
    if id:
        filters.append(AssumptionLandUse.id == id)
    if future_year:
        filters.append(AssumptionLandUse.future_year == future_year)
    return db.query(AssumptionLandUse).filter(*filters).all()


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
