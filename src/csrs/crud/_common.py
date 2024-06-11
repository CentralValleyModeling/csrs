from typing import TypeVar

from sqlalchemy.orm import Session

from ..models import Base

Model = TypeVar("Model", bound=Base)


def common_update(
    db: Session,
    obj: Model,
    raise_on_extra_key: bool = True,
    **kwargs,
) -> Model:
    for k, v in kwargs.items():
        if not hasattr(obj, k) and raise_on_extra_key:
            raise AttributeError(obj, k)
        else:
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def rollback_on_exception(func):
    def _rollback_inner(*args, **kwargs):
        # First find the session in the arguments
        db = None
        for obj in args:
            if isinstance(obj, Session):
                db = obj
        if db is None:
            for _, v in kwargs.items():
                if isinstance(v, Session):
                    db = v
        # Run the fuctions
        try:
            return func(*args, **kwargs)  # Decorated function
        except Exception as e:
            if db:
                db.rollback()
            raise e  # Raise error from decorated func

    return _rollback_inner
