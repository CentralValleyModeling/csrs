import pandss
from sqlalchemy.orm import Session

from .. import models, schemas
from ..enums import PathCategoryEnum
from ..errors import PathCategoryError
from .decorators import rollback_on_exception


@rollback_on_exception
def create(
    db: Session,
    name: str,
    path: str,
    category: str,
    period_type: str,
    interval: str,
    units: str,
    detail: str,
) -> schemas.NamedPath:
    # Check if category is valid
    try:
        category = PathCategoryEnum(category)
    except ValueError:
        raise PathCategoryError(category)
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
    name: str = None,
    path: str | pandss.DatasetPath = None,
    category: str = None,
    id: int = None,
) -> list[schemas.NamedPath]:
    filters = list()
    if name:
        filters.append(models.NamedPath.name == name)
    if path:
        if not isinstance(path, pandss.DatasetPath):
            path = pandss.DatasetPath.from_str(path)
        filters.append(models.NamedPath.path == str(path))
    if category:
        filters.append(models.NamedPath.category == category)
    if id:
        filters.append(models.NamedPath.id == id)
    paths = db.query(models.NamedPath).filter(*filters).all()
    return [schemas.NamedPath.model_validate(p, from_attributes=True) for p in paths]


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
