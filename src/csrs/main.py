from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from . import __version__
from .logger import logger
from .routes import assumptions, forms, paths, runs, scenarios, timeseries

TITLE = "CSRS"
SUMMARY = "CalSim Scenario Results Server"
DESCRIPTION = """
A FastAPI app to serve CalSim3 model results and metadata. Helps you interact with many
CalSim Scenarios at a time.
"""
CONTACT = {
    "name": "California DWR, Central Valley Modeling",
    "url": "https://water.ca.gov/Library/"
    + "Modeling-and-Analysis/Central-Valley-models-and-tools",
}
LISCENSE = {
    "name": "MIT",
    "identifier": "MIT",
}
ENABLE_FORMS = False


def log_app_args():
    logger.info("setting up FastAPI app")
    for name, val in globals():
        # Log the all-uppercase variables in local
        if name.upper() == name:
            logger.info(f"{name}={val}")


# log the environment args
log_app_args()
app = FastAPI(
    title=TITLE,
    summary=SUMMARY,
    version=__version__ or "dev",
    docs_url="/",
    description=DESCRIPTION,
    contact=CONTACT,
    license_info=LISCENSE,
)

app.include_router(timeseries.router)
app.include_router(runs.router)
app.include_router(scenarios.router)
app.include_router(assumptions.router)
app.include_router(paths.router)
if ENABLE_FORMS:
    app.include_router(forms.router)

# TODO move this into a sub-module so the routes can interact with them easily
templates = Jinja2Templates(directory="./templates")
