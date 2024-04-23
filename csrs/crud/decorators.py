from sqlalchemy.orm import Session


def rollback_on_exception(func):
    def inner(*args, **kwargs):
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
            return func(*args, **kwargs)
        except Exception as e:
            if db:
                db.rollback()
            raise e

    return inner
