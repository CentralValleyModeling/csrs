"""Pydantic Models for the CalSim Scenario Server"""

from typing import Self

import pandss as pdss
from pandas import DataFrame, MultiIndex
from pydantic import BaseModel


class Assumption(BaseModel):
    """A single assumption used by a Scenario modeling Scenario. One Assumption
    can be used by multiple Scenarios.
    """

    id: int | None = None
    name: str
    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, kind={self.kind})"

    def __repr__(self) -> str:
        return str(self)


class Scenario(BaseModel):
    """A CalSim modeling Scenario, made up of multiple model runs with the same
    Assumptions. One Scenario can have multiple model Runs to allow for
    improvements and bug fixes over time.
    """

    id: int | None = None
    name: str
    version: str | None = None
    # The attributes below should match the enum AssumptionEnumeration
    land_use: str
    sea_level_rise: str
    hydrology: str
    tucp: str
    dcp: str
    va: str
    south_of_delta: str

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, version={self.version})"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def get_non_assumption_attrs(cls) -> tuple[str]:
        return ("id", "name", "version")

    @classmethod
    def get_assumption_attrs(cls) -> tuple[str]:
        excluded = cls.get_non_assumption_attrs()
        return tuple(a for a in cls.model_fields if a not in excluded)


class Run(BaseModel):
    """A CalSim model run belonging to one Scenario. A model Run can contain
    many timeseries, and many metrics.
    """

    id: int | None = None
    scenario: str
    version: str
    # info
    parent: str | None = None
    children: tuple[str, ...] | tuple = tuple()
    contact: str
    confidential: bool = True
    published: bool = False
    code_version: str
    detail: str

    def __str__(self) -> str:
        c = self.__class__.__name__
        return f"{c}(scenario={self.scenario}, version={self.version})"

    def __repr__(self) -> str:
        return str(self)


class Timeseries(BaseModel):
    """The timeseries data belonging to one model Run."""

    scenario: str
    version: str
    # shadow pandss RegularTimeseries attributes
    path: str
    values: tuple[float, ...]
    dates: tuple[str, ...]
    period_type: str
    units: str
    interval: str

    def __str__(self) -> str:
        c = self.__class__.__name__
        s = self.scenario
        v = self.version
        p = self.path
        return f"{c}(scenario={s}, version={v}, path={p})"

    def __repr__(self) -> str:
        return str(self)

    def to_pandss(self) -> pdss.RegularTimeseries:
        kwargs = self.model_dump(
            exclude=("scenario", "version"),
        )
        if isinstance(self.path, pdss.DatasetPath):
            kwargs["path"] = str(self.path)

        return pdss.RegularTimeseries(**kwargs)

    @classmethod
    def from_pandss(
        cls,
        scenario: str,
        version: str,
        rts: pdss.RegularTimeseries,
    ) -> Self:
        kwargs = rts.to_json()
        return cls(scenario=scenario, version=version, **kwargs)

    def to_frame(self) -> DataFrame:
        df = self.to_pandss().to_frame()
        columns: MultiIndex = df.columns
        df.columns = MultiIndex.from_product(
            columns.levels + [[self.scenario], [self.version]],
            names=tuple(tuple(columns.names) + (("SCENARIO"), ("VERSION"))),
        )
        return df


class NamedPath(BaseModel):
    """A single DSS path, with information about the data it represents."""

    id: int | None = None
    name: str
    path: str
    category: str
    detail: str
    period_type: str
    interval: str
    units: str

    def __str__(self) -> str:
        c = self.__class__.__name__
        return f"{c}(name={self.name}, path={self.path}, category={self.category})"

    def __repr__(self) -> str:
        return str(self)


class Metric(BaseModel):
    """An method of aggregation of timeseries data."""

    id: int | None = None
    name: str
    index_detail: str
    detail: str

    def __str__(self) -> str:
        c = self.__class__.__name__
        return f"{c}(name={self.name})"

    def __repr__(self) -> str:
        return str(self)


class MetricValue(BaseModel):
    """Aggregated values of timeseries data."""

    id: int | None = None
    scenario: str
    run_version: str
    path: str
    metric: str
    indexes: tuple
    values: tuple[float, ...]

    def __str__(self) -> str:
        c = self.__class__.__name__
        s = self.scenario
        v = self.run_version
        m = self.metric
        p = self.path
        return f"{c}(metric={m}, scenario={s}, run_version={v}, path={p})"

    def __repr__(self) -> str:
        return str(self)
