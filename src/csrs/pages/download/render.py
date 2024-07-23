from fastapi import Request
from sqlalchemy.orm import Session

from ... import crud
from .. import loader, templates


def render(request: Request, db: Session):
    return "Hey"
