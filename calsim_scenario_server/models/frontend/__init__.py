from pydantic import BaseModel


class RunModel(BaseModel):
    name: str
    scenario_id: int
    version: str
    contact: str
    confidential: bool
    published: bool
    code_version: str
    detail: str
    predecessor_run_id: int | None


class TimeSeriesValueModel(BaseModel):
    run_id: int
    path_id: int
    timestep_id: int
    value: float


class TimeSeriesBlockModel(BaseModel):
    data: list[TimeSeriesValueModel]


class PathModel(BaseModel):
    path: str
    category: str
    detail: str


class AssumptionModel(BaseModel):
    id: int
    detail: str
