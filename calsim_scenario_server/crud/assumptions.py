from sqlalchemy.orm import Session

from ..logger import logger
from ..models import AssumptionModel
from ..schemas import Assumption
from .decorators import rollback_on_exception


@rollback_on_exception
def create(
    name: str,
    kind: str,
    detail: str,
    db: Session,
) -> Assumption:
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
        raise AttributeError(
            f"assumption given is a duplicate, {dup_name=}, {dup_detail=}.",
        )
    model = AssumptionModel(name=name, kind=kind, detail=detail)
    db.add(model)
    db.commit()
    db.refresh(model)
    return Assumption.model_validate(model, from_attributes=True)


@rollback_on_exception
def read(
    db: Session,
    kind: str = None,
    name: str = None,
    id: int = None,
) -> list[Assumption]:
    logger.debug(f"reading assumptions where {kind=}, {name=}, {id=}")
    filters = list()
    if name:
        filters.append(AssumptionModel.name == name)
    if id:
        filters.append(AssumptionModel.id == id)
    if kind:
        filters.append(AssumptionModel.kind == kind)
    results = db.query(AssumptionModel).filter(*filters).all()
    return [Assumption.model_validate(m, from_attributes=True) for m in results]


def update() -> AssumptionModel:
    raise NotImplementedError()


def delete() -> None:
    raise NotImplementedError()
