import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ...pages import home

router = APIRouter(prefix="/home", include_in_schema=False)
logger = logging.getLogger(__name__)


@router.get("", response_class=HTMLResponse)
async def get_home(request: Request):
    logger.info("getting home page")
    return home.render(request=request)
