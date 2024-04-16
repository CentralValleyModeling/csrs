from datetime import datetime

from sqlalchemy.orm import Session

from ..models import TimestepModel
from ..schemas import Timestep
from .decorators import rollback_on_exception


@rollback_on_exception
def create(db: Session, datetime_str: str) -> Timestep:
    try:
        datetime.fromisoformat(datetime_str)
    except Exception:
        raise AttributeError(f"{datetime_str=} is invalid!")
    ts = TimestepModel(datetime_str=datetime_str)
    db.add(ts)
    db.commit()
    db.refresh(ts)
    return Timestep.model_validate(ts, from_attributes=True)


@rollback_on_exception
def read(db: Session, datetime_str: str = None) -> list[Timestep]:
    filters = list()
    if datetime_str:
        filters.append(TimestepModel.datetime_str == datetime_str)
    tss = db.query(TimestepModel).filter(*filters).all()
    return [Timestep.model_validate(ts, from_attributes=True) for ts in tss]


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
