from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment

from .. import __version__


def library_version_context(request: Request) -> dict[str, str]:
    v = str(__version__)
    if __version__ is None:
        v = "dev"
    return {"library_version": v}


jinja_loader = Jinja2Templates(
    directory=str(Path(__file__).parent),
    context_processors=[
        library_version_context,
    ],
)
ENV: Environment = jinja_loader.env
