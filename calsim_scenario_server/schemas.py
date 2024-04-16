"""Rough dependency tree of the models here

     Assumptions
               │
       Scenarios
               │
            Runs    Paths  Timesteps
               │        │          │
TimeSeriesValues────────┴──────────┤    Metrics
               │                   │          │
    MetricValues───────────────────┴──────────┘
"""

from pydantic import BaseModel


class Foo(BaseModel):
    bar: str


class Assumption(BaseModel):
    id: int | None = None
    name: str
    kind: str
    detail: str


class Scenario(BaseModel):
    id: int | None = None
    name: str
    # The attributes below should match the enum AssumptionEnumeration
    land_use: str
    sea_level_rise: str
    hydrology: str
    tucp: str
    dcp: str
    va: str
    south_of_delta: str

    @classmethod
    def get_assumption_names(cls) -> list:
        return [a for a in cls.model_fields if a not in ("id", "name")]


class NamedPath(BaseModel):
    id: int | None = None
    name: str
    path: str
    category: str
    detail: str


class Timestep(BaseModel):
    id: int | None = None
    datetime_str: str


class Run(BaseModel):
    scenario_id: int
    version: str
    # info
    parent_id: int | None
    children_ids: list[int] | None
    contact: str
    confidential: bool
    published: bool
    code_version: str
    detail: str


class RunOut(Run):
    id: int
    parent_id: int | None


class RunReference(BaseModel):
    id: int
    name: str
    scenario_id: int
    version: str


class TimeSeriesIn(BaseModel):
    run_name: str
    path_name: str
    timesteps: list[str]
    values: list[float]


class TimeSeriesOut(BaseModel):
    id: int
    path: NamedPath
    run: RunOut
    timesteps: list[Timestep]
    values: list[float]


class MetricIn(BaseModel):
    name: str
    index_detail: str
    detail: str


class MetricOut(MetricIn):
    id: int


class MetricValueIn(BaseModel):
    run_name: str
    path_name: str
    metric_name: str
    indexes: list[int]
    values: list[float]


class MetricValueOut(BaseModel):
    id: int
    run: RunOut
    path: NamedPath
    metric: MetricOut
    indexes: list[int]
    values: list[float]
