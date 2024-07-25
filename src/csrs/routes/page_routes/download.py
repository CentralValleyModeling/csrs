import io
import json

import pandas as pd
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session

from ... import crud
from ...database import DATABASE, get_db
from ...logger import logger
from ...pages import download

router = APIRouter(prefix="/download", include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
async def page_download(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    runs = crud.runs.read(db)
    return download.render(request, runs=runs)


@router.get("/run", response_class=StreamingResponse)
async def download_run(
    scenario: str,
    version: str,
    request: Request,
    file_type: str = "csv",
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")

    file_content = io.StringIO()
    if file_type.lower() == "csv":
        timeseries = crud.timeseries.read_all_for_run(
            db,
            scenario=scenario,
            version=version,
        )
        frames = [ts.to_frame() for ts in timeseries]
        df = pd.concat(frames, axis=1)
        df.to_csv(file_content)
        media_type = "text/csv"
    elif file_type.lower() == "json":
        (run,) = crud.runs.read(db, scenario=scenario, version=version)
        (scen,) = crud.scenarios.read(db, name=scenario)
        assumptions = crud.assumptions.read_for_scenario(db, scenario=scenario)
        paths = crud.paths.read_paths_in_run(db, run_id=run.id)
        file_str = json.dumps(
            dict(
                run=run.model_dump(),
                scenario=scen.model_dump(),
                assumptions=[a.model_dump() for a in assumptions],
                paths=[p.model_dump() for p in paths],
            ),
            indent=4,
        )
        file_content.write(file_str)
        media_type = "text/json"
    else:
        raise NotImplementedError(f"{file_type=}")
    file_content.seek(0)
    filename = f"{scenario}-{version}.{file_type}"
    return StreamingResponse(
        file_content,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )
