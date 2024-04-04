from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...models import AssumptionDeltaConveyanceProject


def create(
    name: str,
    detail: str,
    db: Session,
) -> AssumptionDeltaConveyanceProject:
    # check if it exists already
    dup_name = (
        db.query(AssumptionDeltaConveyanceProject).filter_by(name=name).first()
        is not None
    )
    dup_detail = (
        db.query(AssumptionDeltaConveyanceProject).filter_by(detail=detail).first()
        is not None
    )
    if dup_name or dup_detail:
        raise HTTPException(
            status_code=400,
            detail=f"assumption given is a duplicate, {dup_name=}, {dup_detail=}.",
        )
    model = AssumptionDeltaConveyanceProject(name=name, detail=detail)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[AssumptionDeltaConveyanceProject]:
    filters = list()
    if name:
        filters.append(AssumptionDeltaConveyanceProject.name == name)
    if id:
        filters.append(AssumptionDeltaConveyanceProject.id == id)
    return db.query(AssumptionDeltaConveyanceProject).filter(*filters).all()


def update() -> AssumptionDeltaConveyanceProject:
    raise NotImplementedError()


def delete() -> None:
    raise NotImplementedError()
