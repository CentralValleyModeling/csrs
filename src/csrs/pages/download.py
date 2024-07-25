from fastapi import Request

from .. import schemas
from . import loader
from .edit import ALLOW_EDITING_VIA_FORMS


def render(
    request: Request,
    runs: list[schemas.Run],
):
    desc = loader.ENV.get_template("static/descriptions/download.jinja").render(
        request=request
    )
    return loader.jinja_loader.TemplateResponse(
        "templates/download.jinja",
        context=dict(
            page_title="Download",
            page_description=desc,
            request=request,
            runs=runs,
            edit_on=ALLOW_EDITING_VIA_FORMS,
        ),
    )
