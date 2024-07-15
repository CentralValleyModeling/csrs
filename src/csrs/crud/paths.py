from sqlalchemy.orm import Session

from .. import models, schemas
from ..logger import logger
from ._common import common_update, rollback_on_exception


@rollback_on_exception
def create(
    db: Session,
    *,
    name: str,
    path: str,
    category: str,
    period_type: str,
    interval: str,
    units: str,
    detail: str,
) -> schemas.NamedPath:
    logger.info(f"creating new named path {name=}, {path=}")
    # Check if category is valid
    path = models.NamedPath(
        name=name,
        path=str(path),
        category=category,
        period_type=period_type,
        interval=interval,
        units=units,
        detail=detail,
    )
    db.add(path)
    db.commit()
    db.refresh(path)
    return schemas.NamedPath.model_validate(path, from_attributes=True)


@rollback_on_exception
def read(
    db: Session,
    *,
    name: str = None,
    path: str = None,
    category: str = None,
    id: int = None,
) -> list[schemas.NamedPath]:
    logger.info(f"reading named path where {name=}, {category=}, {path=}")
    filters = list()
    if name:
        filters.append(models.NamedPath.name == name)
    if path:
        filters.append(models.NamedPath.path == str(path))
    if category:
        filters.append(models.NamedPath.category == category)
    if id:
        filters.append(models.NamedPath.id == id)
    paths = db.query(models.NamedPath).filter(*filters).all()
    return [schemas.NamedPath.model_validate(p, from_attributes=True) for p in paths]


def update(
    db: Session,
    id: int,
    **kwargs,
) -> schemas.NamedPath:
    obj = db.query(models.NamedPath).filter(models.NamedPath.id == id).first()
    if obj:
        updated = common_update(db, obj, **kwargs)
    else:
        raise ValueError(f"Cannot find Assumption with {id=}")
    return updated


def delete(
    db: Session,
    id: int,
) -> None:
    logger.info(f"deleteing path where {id=}")
    obj = db.query(models.NamedPath).filter(models.NamedPath.id == id).first()
    if not obj:
        raise ValueError(f"Cannot find NamedPath with {id=}")
    db.query(models.NamedPath).filter(models.NamedPath.id == id).delete()
    db.commit()
