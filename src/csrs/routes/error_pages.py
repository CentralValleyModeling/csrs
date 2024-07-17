from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from ..templates import templates

router = APIRouter(prefix="/errors", include_in_schema=False)


@router.get("/404", response_class=HTMLResponse)
async def custom_404_handler(request, __):
    return templates.TemplateResponse(
        "errors/404.jinja",
        {"request": request},
    )
