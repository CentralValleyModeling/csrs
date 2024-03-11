import pandss as pdss
from fastapi import HTTPException

from .database import StudyDatabase


async def read_rts_from_b(
    db: StudyDatabase,
    b_part: str,
    file_key: str,
) -> dict[str, pdss.RegularTimeseries]:
    path = pdss.DatasetPath(b=b_part)
    payload = dict()
    for study in db.studies:
        src = getattr(study, file_key)
        # Read data
        with pdss.DSS(src) as dss:
            data = [rts for rts in dss.read_multiple_rts(path)]
        # Handle errors if 0, or more than 1 dataset was matched
        if len(data) != 1:
            if len(data) == 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"{b_part=} matches no data in {file_key}",
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"{b_part=} matches more than one timeseries in {file_key}",
                )
        payload[study.display_name] = data[0]
    return payload
