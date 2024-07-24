from fastapi import Request

from .loader import jinja_loader


def error_404(request: Request):
    return jinja_loader.TemplateResponse(
        "/static/errors/404.jinja",
        dict(request=request),
        status_code=404,
    )
