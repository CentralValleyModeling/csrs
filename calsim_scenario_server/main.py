from fastapi import FastAPI

from . import metadata, routers

kwargs = metadata.from_json()
app = FastAPI(**kwargs)
app.include_router(routers.excel.router)
app.include_router(routers.python.router)
