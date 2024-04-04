from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...models import AssumptionVoluntaryAgreements


def create(
    name: str,
    detail: str,
    db: Session,
) -> AssumptionVoluntaryAgreements:
    # check if it exists already
    dup_name = (
        db.query(AssumptionVoluntaryAgreements).filter_by(name=name).first() is not None
    )
    dup_detail = (
        db.query(AssumptionVoluntaryAgreements).filter_by(detail=detail).first()
        is not None
    )
    if dup_name or dup_detail:
        raise HTTPException(
            status_code=400,
            detail=f"assumption given is a duplicate, {dup_name=}, {dup_detail=}.",
        )
    model = AssumptionVoluntaryAgreements(name=name, detail=detail)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[AssumptionVoluntaryAgreements]:
    filters = list()
    if name:
        filters.append(AssumptionVoluntaryAgreements.name == name)
    if id:
        filters.append(AssumptionVoluntaryAgreements.id == id)
    return db.query(AssumptionVoluntaryAgreements).filter(*filters).all()


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
