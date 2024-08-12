from fastapi import Request

from .. import schemas
from ..database import db_cfg
from . import loader


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
            edit_on=db_cfg.allow_editing_via_forms,
        ),
    )
