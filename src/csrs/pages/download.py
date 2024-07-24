from fastapi import Request
from sqlalchemy.orm import Session

from .. import crud
from . import loader, templates
from .edit import ALLOW_EDITING_VIA_FORMS


def render(request: Request, db: Session):
    return loader.jinja_loader.TemplateResponse(
        "templates/download.jinja",
        context=dict(
            request=request,
            edit_on=ALLOW_EDITING_VIA_FORMS,
        ),
    )
