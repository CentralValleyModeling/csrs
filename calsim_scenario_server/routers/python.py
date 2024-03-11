from fastapi import APIRouter, Depends, HTTPException

from ..crud import read_rts_from_b
from ..database import StudyDatabase, get_db
from ..util import cy_annual_exceedance, exceedance, rts_to_json, wy_annual_exceedance

router = APIRouter(prefix="/py")


@router.get("/rts")
async def get_regular_timeseries(
    b_part: str,
    dss: str = "dv",
    db: StudyDatabase = Depends(get_db),
):
    if not b_part:
        raise HTTPException(status_code=400, detail="Parameter is required")
    rts_dict = await read_rts_from_b(db, b_part, dss)
    return {k: rts_to_json(rts) for k, rts in rts_dict.items()}


@router.get("/exceedance")
async def get_exceedance_b(
    b_part: str,
    dss: str = "dv",
    db: StudyDatabase = Depends(get_db),
):
    if not b_part:
        raise HTTPException(status_code=400, detail="Parameter is required")
    rts_dict = await read_rts_from_b(db, b_part, dss)
    return {k: exceedance(rts) for k, rts in rts_dict.items()}


@router.get("/annual_exceedance")
async def get_annual_exceedance_b(
    b_part: str,
    file: str = "dv",
    dss: str = "wy",
    db: StudyDatabase = Depends(get_db),
):
    if not b_part:
        raise HTTPException(status_code=400, detail="Parameter is required")
    rts_dict = await read_rts_from_b(db, b_part, file)
    if dss.lower() == "cy":
        calc = cy_annual_exceedance
    else:
        calc = wy_annual_exceedance
    return {k: calc(rts) for k, rts in rts_dict.items()}
