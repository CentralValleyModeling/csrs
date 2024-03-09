from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException

from .crud import read_rts_from_b
from .database import StudyDatabase
from .util import cy_annual_exceedance, exceedance, rts_to_json, wy_annual_exceedance

app = FastAPI()


def get_db():
    here = Path("C:/Users/zroy/Documents/_Python/calsim_scenario_server")
    db = StudyDatabase(config=here / "database/distributed_repo.toml")
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def get_main_page(db: StudyDatabase = Depends(get_db)):
    studies = db.get_studies()
    return {"page": "CalSim3 Scenario manager", "studies": studies}


@app.get("/rts/{file_key}/b/{b_part}")
async def get_regular_timeseries(
    file_key: str,
    b_part: str,
    db: StudyDatabase = Depends(get_db),
):
    if not b_part:
        raise HTTPException(status_code=400, detail="Parameter is required")
    rts_dict = await read_rts_from_b(db, b_part, file_key)
    return {k: rts_to_json(rts) for k, rts in rts_dict.items()}


@app.get("/exceedance/{file_key}/b/{b_part}")
async def get_exceedance_b(
    file_key: str,
    b_part: str,
    db: StudyDatabase = Depends(get_db),
):
    if not b_part:
        raise HTTPException(status_code=400, detail="Parameter is required")
    rts_dict = await read_rts_from_b(db, b_part, file_key)
    return {k: exceedance(rts) for k, rts in rts_dict.items()}


@app.get("/annual_exceedance/{file_key}/b/{b_part}")
async def get_annual_exceedance_b(
    file_key: str,
    b_part: str,
    year_type: str = "wy",
    db: StudyDatabase = Depends(get_db),
):
    if not b_part:
        raise HTTPException(status_code=400, detail="Parameter is required")
    rts_dict = await read_rts_from_b(db, b_part, file_key)
    if year_type.lower() == "cy":
        calc = cy_annual_exceedance
    else:
        calc = wy_annual_exceedance
    return {k: calc(rts) for k, rts in rts_dict.items()}
