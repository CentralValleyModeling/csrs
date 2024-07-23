from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ...pages import Home

router = APIRouter(prefix="/home", include_in_schema=False)


@router.get("", response_class=HTMLResponse)
async def get_home(request: Request):
    return HTMLResponse(Home(request=request))
