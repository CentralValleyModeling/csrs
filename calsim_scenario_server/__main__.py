from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from .routes import assumptions, forms, paths, runs, scenarios, timeseries

app = FastAPI(
    title="CalSim3 Scenario Server",
    summary="A FastAPI app to serve CalSim3 inputs and results.",
    version="0.0.2",
    docs_url="/",
)

ENABLE_FORMS = False

app.include_router(scenarios.router)
app.include_router(paths.router)
app.include_router(runs.router)
app.include_router(assumptions.router)
app.include_router(timeseries.router)
if ENABLE_FORMS:
    app.include_router(forms.router)

# TODO move this into a sub-module so the routes can interact with them easily
templates = Jinja2Templates(directory="./templates")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
