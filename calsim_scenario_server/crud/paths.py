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
    detail: str,
) -> schemas.NamedDatasetPath:
    # Check if category is valid
    try:
        category = PathCategoryEnum(category)
    except ValueError:
        raise PathCategoryError(category)
    # Check if pathstr is valid
    dsp = pandss.DatasetPath.from_str(path)
    path_str = f"/CALSIM/{dsp.b}/{dsp.c}//{dsp.e}/SERVER/"
    path = models.NamedDatasetPath(
        name=name,
        path=path_str,
        category=category,
        detail=detail,
    )
    db.add(path)
    db.commit()
    db.refresh(path)
    return schemas.NamedDatasetPath.model_validate(path, from_attributes=True)


@rollback_on_exception
def read(
    db: Session,
    name: str = None,
    path: str = None,
    category: str = None,
    id: int = None,
) -> list[schemas.NamedDatasetPath]:
    filters = list()
    if name:
        filters.append(models.NamedDatasetPath.name == name)
    if path:
        dsp = pandss.DatasetPath.from_str(path)
        path_str = f"/CALSIM/{dsp.b}/{dsp.c}//{dsp.e}/SERVER/"
        filters.append(models.NamedDatasetPath.path == path_str)
    if category:
        filters.append(models.NamedDatasetPath.category == category)
    if id:
        filters.append(models.NamedDatasetPath.id == id)
    paths = db.query(models.NamedDatasetPath).filter(*filters).all()
    return [
        schemas.NamedDatasetPath.model_validate(p, from_attributes=True) for p in paths
    ]


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
