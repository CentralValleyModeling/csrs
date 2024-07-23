from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ...database import get_db
from ...logger import logger
from ...pages import download

router = APIRouter(prefix="/download", include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
async def page_download(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return download.render(request, db)
