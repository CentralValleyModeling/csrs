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
    scenario: str
    version: str
    # info
    parent_id: int | None
    children_ids: tuple[int] | tuple
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
    timesteps: tuple[str]
    values: tuple[float]


class TimeSeriesOut(BaseModel):
    id: int
    path: NamedPath
    run: RunOut
    timesteps: tuple[Timestep]
    values: tuple[float]


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
    indexes: tuple[int]
    values: tuple[float]


class MetricValueOut(BaseModel):
    id: int
    run: RunOut
    path: NamedPath
    metric: MetricOut
    indexes: tuple[int]
    values: tuple[float]
