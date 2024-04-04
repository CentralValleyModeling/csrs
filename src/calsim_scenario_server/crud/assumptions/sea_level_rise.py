from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...models import AssumptionSeaLevelRise


def create(
    name: str,
    detail: str,
    centimeters: float,
    db: Session,
) -> AssumptionSeaLevelRise:
    # check if it exists already
    dup_name = db.query(AssumptionSeaLevelRise).filter_by(name=name).first() is not None
    dup_detail = (
        db.query(AssumptionSeaLevelRise).filter_by(detail=detail).first() is not None
    )
    if dup_name or dup_detail:
        raise HTTPException(
            status_code=400,
            detail=f"assumption given is a duplicate, {dup_name=}, {dup_detail=}.",
        )
    model = AssumptionSeaLevelRise(name=name, detail=detail, centimeters=centimeters)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def read(
    db: Session,
    name: str = None,
    centimeters: float = None,
    id: int = None,
) -> list[AssumptionSeaLevelRise]:
    filters = list()
    if name:
        filters.append(AssumptionSeaLevelRise.name == name)
    if id:
        filters.append(AssumptionSeaLevelRise.id == id)
    if centimeters:
        filters.append(AssumptionSeaLevelRise.centimeters == centimeters)
    return db.query(AssumptionSeaLevelRise).filter(*filters).all()


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
