from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session

from ...database import ALLOW_DOWNLOAD, DATABASE, get_db
from ...logger import logger
from ...pages import database as database_page

router = APIRouter(prefix="/database", include_in_schema=False)


async def page_database(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return database_page.render(request)


async def database_download(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")

    def stream(f):
        with open(f, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(
        stream(DATABASE),
        media_type="application/vnd.sqlite3",
        headers={
            "Content-Disposition": f"attachment; filename={DATABASE.name}",
            "Content-Length": str(DATABASE.stat().st_size),
        },
    )


if ALLOW_DOWNLOAD:
    router.get("/", response_class=HTMLResponse)(page_database)
    router.get("/download", response_class=StreamingResponse)(database_download)
