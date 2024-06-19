from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from . import __version__
from .database import DATABASE
from .logger import logger
from .routes import assumptions, forms, home, paths, runs, scenarios, timeseries

TITLE = "CSRS"
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

app.include_router(home.router)
app.include_router(timeseries.router)
app.include_router(runs.router)
app.include_router(scenarios.router)
app.include_router(assumptions.router)
app.include_router(paths.router)
app.include_router(forms.router)

log_global_args()


@app.get(
    "/",
    response_class=RedirectResponse,
    status_code=302,
    include_in_schema=False,
)
async def redirect_home():
    return "/home"
