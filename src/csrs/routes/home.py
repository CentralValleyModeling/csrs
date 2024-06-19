from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..templates import templates

router = APIRouter(prefix="/home", include_in_schema=False)


@router.get("", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.jinja", {"request": request})
