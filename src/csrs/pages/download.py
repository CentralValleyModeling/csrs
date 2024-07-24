from fastapi import Request

from .. import schemas
from . import loader
from .edit import ALLOW_EDITING_VIA_FORMS


def render(
    request: Request,
    runs: list[schemas.Run],
):
    return loader.jinja_loader.TemplateResponse(
        "templates/download.jinja",
        context=dict(
            page_title="Download",
            page_description="Download the <code>Timeseries</code> data as a <code>CSV</code>, or the <code>Run</code> and it's metadata.",
            request=request,
            runs=runs,
            edit_on=ALLOW_EDITING_VIA_FORMS,
        ),
    )
