from pydantic import BaseModel


class TimeSeriesValueModel(BaseModel):
    run_id: int
    path_id: int
    timestep_id: int
    value: float


class TimeSeriesBlockModel(BaseModel):
    data: list[TimeSeriesValueModel]
