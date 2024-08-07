from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse

from . import config, routes
from .logger import logger
from .pages import errors


def create_app() -> FastAPI:
    app_cfg = config.AppConfig()
    app = FastAPI(**app_cfg.model_dump())
    app.include_router(routes.page_routes.home.router)
    app.include_router(routes.timeseries.router)
    app.include_router(routes.runs.router)
    app.include_router(routes.scenarios.router)
    app.include_router(routes.assumptions.router)
    app.include_router(routes.paths.router)
    app.include_router(routes.page_routes.edit.router)
    app.include_router(routes.page_routes.download.router)
    app.include_router(routes.page_routes.database.router)
    return app


app = create_app()


@app.get("/", response_class=RedirectResponse, status_code=302, include_in_schema=False)
async def redirect_home():
    return RedirectResponse("/home")


@app.exception_handler(404)
async def custom_404_handler(request: Request, _):
    user_agent = request.headers.get("User-Agent", "")
    if "bot" in user_agent.lower():
        return HTTPException(status_code=404)
    else:
        logger.error("rendering HTML 404 page")
        return errors.error_404(request=request)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    here = Path().parent
    f = here / "pages/static/img/calsim3_icon.svg"
    if f.exists():
        return FileResponse(str(f))
    else:
        return (
            "https://raw.githubusercontent.com/CentralValleyModeling/"
            + "static-assets/main/images/calsim3_icon.svg"
        )
