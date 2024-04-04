from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...models import AssumptionTUCP


def create(
    name: str,
    detail: str,
    db: Session,
) -> AssumptionTUCP:
    # check if it exists already
    dup_name = db.query(AssumptionTUCP).filter_by(name=name).first() is not None
    dup_detail = db.query(AssumptionTUCP).filter_by(detail=detail).first() is not None
    if dup_name or dup_detail:
        raise HTTPException(
            status_code=400,
            detail=f"assumption given is a duplicate, {dup_name=}, {dup_detail=}.",
        )
    model = AssumptionTUCP(name=name, detail=detail)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[AssumptionTUCP]:
    filters = list()
    if name:
        filters.append(AssumptionTUCP.name == name)
    if id:
        filters.append(AssumptionTUCP.id == id)
    return db.query(AssumptionTUCP).filter(*filters).all()


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
