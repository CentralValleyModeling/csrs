from fastapi import Request

from .edit import ALLOW_EDITING_VIA_FORMS
from .loader import jinja_loader


def render(request: Request):
    return jinja_loader.TemplateResponse(
        "templates/home.jinja",
        context=dict(
            request=request,
            edit_on=ALLOW_EDITING_VIA_FORMS,
        ),
    )
