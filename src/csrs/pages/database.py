from fastapi import Request

from . import loader


def render(
    request: Request,
):
    desc = loader.ENV.get_template("static/descriptions/database.jinja").render(
        request=request
    )
    return loader.jinja_loader.TemplateResponse(
        "templates/database.jinja",
        context=dict(
            page_title="Database Download",
            page_description=desc,
            request=request,
        ),
    )
