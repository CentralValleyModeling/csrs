from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from . import __version__, routes
from .database import get_database_url
from .logger import logger
from .pages import jinja_loader

TITLE = "CSRS"
DATABASE = get_database_url()
SUMMARY = "CalSim Scenario Results Server"
DESCRIPTION = """\
A FastAPI app to serve CalSim3 model results and metadata. Helps you interact with many
CalSim Scenarios at a time."""
CONTACT = {
    "name": "California DWR, Central Valley Modeling",
    "url": "https://water.ca.gov/Library/"
    + "Modeling-and-Analysis/Central-Valley-models-and-tools",
}
LISCENSE = {
    "name": "MIT",
    "identifier": "MIT",
}


def log_global_args():
    logger.info("setting up FastAPI app")
    for name, val in globals().items():
        # Log the all-uppercase variables in local
        if name.upper() == name:
            val = str(val)
            if "\n" in val:
                val = val.split("\n")[0] + "..."
            logger.info(f"{name}={val}")
            if isinstance(val, Path):
                logger.info(f"above path exists: {val.exists()}")


# log the environment args
app = FastAPI(
    title=TITLE,
    summary=SUMMARY,
    version=__version__ or "dev",
    docs_url="/docs",
    description=DESCRIPTION,
    contact=CONTACT,
    license_info=LISCENSE,
)

app.include_router(routes.pages.home.router)
app.include_router(routes.timeseries.router)
app.include_router(routes.runs.router)
app.include_router(routes.scenarios.router)
app.include_router(routes.assumptions.router)
app.include_router(routes.paths.router)
app.include_router(routes.pages.edit.router)
app.include_router(routes.pages.download.router)


log_global_args()


@app.get("/", response_class=RedirectResponse, status_code=302, include_in_schema=False)
async def redirect_home():
    return RedirectResponse("/home")


@app.exception_handler(404)
async def custom_404_handler(request: Request, __):
    # TODO: 2024-07-23 Make this detection of API/Page interaction better
    if request.url.path.startswith(("/edit", "/download")):
        logger.error("rendering HTML 404 page")
        return jinja_loader.TemplateResponse(
            "/static/errors/404.jinja",
            dict(request=request),
            status_code=404,
        )

    else:
        return HTTPException(status_code=404)
