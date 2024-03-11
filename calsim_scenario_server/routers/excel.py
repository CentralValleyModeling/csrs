from xml.etree.ElementTree import Element, tostring

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException

from ..crud import read_rts_from_b
from ..database import StudyDatabase, get_db
from ..util import cy_annual_exceedance, rts_to_xml, wy_annual_exceedance

router = APIRouter(prefix="/xl")


@router.get("/rts")
async def get_regular_timeseries(
    b_part: str,
    dss: str = "dv",
    db: StudyDatabase = Depends(get_db),
):
    if not b_part:
        raise HTTPException(status_code=400, detail="Parameter is required")
    rts_dict = await read_rts_from_b(db, b_part, dss)
    rts_dict = {k: rts_to_xml(rts) for k, rts in rts_dict.items()}

    root = Element("root")

    for v in rts_dict.values():
        root.append(v)

    return tostring(root)


@router.get("/annual_exceedance")
async def get_annual_exceedance_b(
    b_part: str,
    dss: str = "dv",
    year_type: str = "wy",
    db: StudyDatabase = Depends(get_db),
):
    if not b_part:
        raise HTTPException(status_code=400, detail="Parameter is required")
    rts_dict = await read_rts_from_b(db, b_part, dss)
    if year_type.lower() == "cy":
        calc = cy_annual_exceedance
    else:
        calc = wy_annual_exceedance
    d = {k: calc(rts) for k, rts in rts_dict.items()}

    d = {k: pd.DataFrame.from_dict(sub_d) for k, sub_d in d.items()}

    for k, df in d.items():
        df = df.set_index("exceedance").reindex(
            np.arange(0.0, 1.0, 0.01),
            method="nearest",
        )
        df.columns = [k]
        d[k] = df
    s = pd.concat(d.values(), axis=1).to_csv(quotechar='"')

    return s
