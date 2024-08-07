from fastapi import Request

from .edit import editing_cfg
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
            edit_on=editing_cfg.allow_editing_via_forms,
        ),
    )
