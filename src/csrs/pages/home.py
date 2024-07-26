from fastapi import Request

from .edit import ALLOW_EDITING_VIA_FORMS
from .loader import ENV, jinja_loader


def render(request: Request):
    description = ENV.get_template("static/descriptions/home.jinja").render(
        context=dict(request=request)
    )
    return jinja_loader.TemplateResponse(
        "templates/home.jinja",
        context=dict(
            page_title="CalSim Scenario Results Server",
            page_description=description,
            request=request,
            edit_on=ALLOW_EDITING_VIA_FORMS,
        ),
    )
