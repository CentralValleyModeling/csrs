import io
import json
import logging

import pandas as pd
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session

from ... import crud, errors, models, schemas
from ...database import get_db
from ...pages import download

router = APIRouter(prefix="/download", include_in_schema=False)
logger = logging.getLogger(__name__)


@router.get("/", response_class=HTMLResponse)
async def page_download(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    runs = crud.runs.read(db)
    return download.render(request, runs=runs)


def slow_lossy_concat(frames: list[pd.DataFrame]) -> pd.DataFrame:
    df = frames.pop()
    for _df in frames:
        try:
            df = pd.concat([df, _df], axis=1)
        except Exception:
            info = "\t\n".join(df.columns[0])
            logger.info(f"error when concatenaing dataframe:\n{info}")
    return df


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
        try:
            timeseries = crud.timeseries.read_all_for_run(
                db,
                scenario=scenario,
                version=version,
            )
            frames = [ts.to_frame() for ts in timeseries]
            if len(frames) == 0:
                raise errors.EmptyLookupError(models.TimeseriesLedger)
            try:
                df = pd.concat(frames, axis=1)
            except Exception as e:
                logger.error(
                    f"{type(e).__name__} occurred when concatenating all the data,"
                    + " trying again with a slower method"
                )
                df = slow_lossy_concat(frames)
        except errors.EmptyLookupError as e:
            # return an empty dataset
            logger.error(
                f"{type(e).__name__} occurred when reading timeseries data for:"
                + f"{scenario=}, {version=}, returning empty csv"
            )
            ts = schemas.Timeseries(
                scenario=scenario,
                version=version,
                path="/.*/.*/.*/.*/.*/.*/",
                values=(0.0,),
                dates=("1921-10-31",),
                period_type="PER-AVER",
                units="NONE",
                interval="1MON",
            )
            df = ts.to_frame()
            df = df.drop(df.index[0])

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
