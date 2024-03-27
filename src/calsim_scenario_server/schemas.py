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

from pydantic import BaseModel, Field


class AssumptionIn(BaseModel):
    name: str
    detail: str
    additional_metadata: dict = Field(default_factory=dict)


class AssumptionOut(AssumptionIn):
    id: int


class ScenarioIn(BaseModel):
    name: str
    assumptions_used: list[AssumptionIn]


class ScenarioOut(ScenarioIn):
    id: int


class PathIn(BaseModel):
    name: str
    path: str
    category: str
    detail: str


class PathOut(PathIn):
    id: int = None


class TimeStepIn(BaseModel):
    datetime_str: str


class TimeStepOut(TimeStepIn):
    id: int


class RunIn(BaseModel):
    name: str
    scenario_id: int
    version: str
    # metadata
    predecessor_run_name: str | None
    contact: str
    confidential: bool
    pubished: bool
    code_version: str
    detail: str


class RunOut(RunIn):
    id: int
    predecessor_run_id: int | None


class TimeSeriesIn(BaseModel):
    run_name: str
    path_name: str
    timesteps: list[str]
    values: list[float]


class TimeSeriesOut(BaseModel):
    id: int
    path: PathOut
    run: RunOut
    timesteps: list[TimeStepOut]
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
    path: PathOut
    metric: MetricOut
    indexes: list[int]
    values: list[float]
