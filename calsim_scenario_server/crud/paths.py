import pandss
from sqlalchemy.orm import Session

from ..enum import PathCategoryEnum
from ..models import NamedPathModel
from ..schemas import NamedDatasetPath
from .decorators import rollback_on_exception


@rollback_on_exception
def create(
    db: Session,
    name: str,
    path: str,
    category: str,
    detail: str,
) -> NamedDatasetPath:
    # Check if category is valid
    try:
        category = PathCategoryEnum(category)
    except ValueError:
        raise AttributeError(
            f"{category} is not a valid category, must be one of:\n"
            + "\n".join(PathCategoryEnum._member_names_)
        )
    # Check if pathstr is valid
    try:
        pandss.DatasetPath.from_str(path)
    except Exception:
        raise AttributeError(f"{path=} cannot be converted to DSS path")
    path = NamedPathModel(
        name=name,
        path=path,
        category=category,
        detail=detail,
    )
    db.add(path)
    db.commit()
    db.refresh(path)
    return NamedDatasetPath.model_validate(path, from_attributes=True)


@rollback_on_exception
def read(
    db: Session,
    name: str = None,
    path: str = None,
    category: str = None,
    id: int = None,
) -> list[NamedDatasetPath]:
    filters = list()
    if name:
        filters.append(NamedPathModel.name == name)
    if path:
        filters.append(NamedPathModel.path == path)
    if category:
        filters.append(NamedPathModel.category == category)
    if id:
        filters.append(NamedPathModel.id == id)
    paths = db.query(NamedPathModel).filter(*filters).all()
    return [NamedDatasetPath.model_validate(p, from_attributes=True) for p in paths]

    raise NotImplementedError()


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
