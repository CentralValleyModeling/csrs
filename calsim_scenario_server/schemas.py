"""Pydantic Models for the CalSim Scenario Server"""

from pydantic import BaseModel


class Assumption(BaseModel):
    """A single assumption used by a Scenario modeling Scenario. One Assumption
    can be used by multiple Scenarios.
    """

    id: int | None = None
    name: str
    kind: str
    detail: str


class Scenario(BaseModel):
    """A CalSim modeling Scenario, made up of multiple model runs with the same
    Assumptions. One Scenario can have multiple model Runs to allow for
    improvements and bug fixes over time."""

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


class Run(BaseModel):
    """A CalSim model run belonging to one Scenario. A model Run can contain
    many timeseries, and many metrics."""

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


class NamedDatasetPath(BaseModel):
    """A single DSS path, with information about the data it represents."""

    id: int | None = None
    name: str
    path: str
    category: str
    detail: str


class Metric(BaseModel):
    """An method of aggregation of timeseries data."""

    id: int | None = None
    name: str
    index_detail: str
    detail: str


class MetricValue(BaseModel):
    """Aggregated values of timeseries data."""

    id: int | None = None
    scenario: str
    run_version: str
    path: str
    metric: str
    indexes: tuple[int]
    values: tuple[float]
