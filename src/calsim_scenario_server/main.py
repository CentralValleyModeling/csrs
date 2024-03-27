from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from . import __version__
from .routes import assumptions, forms, paths, runs, scenarios, timeseries, timesteps

TITLE = "CalSim-Results Server"
SUMMARY = "A FastAPI app to serve CalSim3 model results and metadata."
DESCRIPTION = """
Helps you to interact with the CalSim Scnario Database.
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


app = FastAPI(
    title=TITLE,
    summary=SUMMARY,
    version=__version__,
    docs_url="/",
    description=DESCRIPTION,
    contact=CONTACT,
    license_info=LISCENSE,
)

ENABLE_FORMS = False

app.include_router(timeseries.router)
app.include_router(runs.router)
app.include_router(scenarios.router)
app.include_router(assumptions.router)
app.include_router(paths.router)
app.include_router(timesteps.router)
if ENABLE_FORMS:
    app.include_router(forms.router)

# TODO move this into a sub-module so the routes can interact with them easily
templates = Jinja2Templates(directory="./templates")
