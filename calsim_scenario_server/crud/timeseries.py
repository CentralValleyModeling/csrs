from datetime import datetime

from sqlalchemy.orm import Session

from .. import models, schemas
from ..logger import logger
from .decorators import rollback_on_exception


@rollback_on_exception
def create(
    db: Session,
    scenario: str = None,
    version: str = None,
):

    return None


@rollback_on_exception
def read(
    db: Session,
    scenario: str = None,
    version: str = None,
) -> list:

    return None


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
