"""Rough dependency tree of the models here

     Assumptions
               │
       Scenarios
               │
            Runs    Paths  Timesteps
               │        │          │
TimeSeriesValues────────┤──────────┘   Metrics
               │        │                     │
    MetricValues──────────────────────────────┘
"""

from pydantic import BaseModel


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
    def get_assumption_names(cls) -> tuple:
        return tuple(a for a in cls.model_fields if a not in ("id", "name"))


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
    id: int | None = None
    scenario: str
    version: str
    # info
    parent_id: int | None = None
    children_ids: tuple[int] | tuple = tuple()
    contact: str
    confidential: bool = True
    published: bool = False
    code_version: str
    detail: str


class TimeSeries(BaseModel):
    id: int | None = None
    scenario: str
    run_version: str
    path: str
    timesteps: tuple[str]
    values: tuple[float]
    timesteps: tuple[Timestep]


class Metric(BaseModel):
    id: int | None = None
    name: str
    index_detail: str
    detail: str


class MetricValue(BaseModel):
    id: int | None = None
    scenario: str
    run_version: str
    path: str
    metric: str
    indexes: tuple[int]
    values: tuple[float]
