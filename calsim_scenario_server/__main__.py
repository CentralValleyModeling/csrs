from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from .database import engine
from .models import Base
from .routes import forms, paths, runs, scenarios

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
if ENABLE_FORMS:
    app.include_router(forms.router)

templates = Jinja2Templates(directory="./templates")
# Create database tables
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
