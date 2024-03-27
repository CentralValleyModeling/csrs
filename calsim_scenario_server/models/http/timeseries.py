from pydantic import BaseModel


class TimeSeriesValueModel(BaseModel):
    run_id: int
    path_id: int
    timestep_id: int
    value: float


class TimeSeriesBlockModel(BaseModel):
    count: int
    run_ids: list[int]
    path_ids: list[int]
    timestep_ids: list[int]
    values: list[float]
