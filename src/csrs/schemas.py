"""Pydantic Models for the CalSim Scenario Server"""

from typing import TYPE_CHECKING, Self

from pandas import DataFrame, MultiIndex
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    # Optional dependency
    import pandss as pdss


class CSRS_Model(BaseModel):
    def __str__(self) -> str:
        s = self.__class__.__name__
        attrs = list()
        for name, field in self.model_fields.items():
            if field.repr:
                attrs.append(f"{name}={getattr(self, name)}")
        if attrs:
            attrs = ", ".join(attrs)

        return f"{s}({attrs})"


class Assumption(CSRS_Model):
    """A single assumption used by a Scenario modeling Scenario. One Assumption
    can be used by multiple Scenarios.
    """

    id: int | None = Field(default=None, repr=False)
    name: str
    kind: str
    detail: str = Field(repr=False)


class Scenario(CSRS_Model):
    """A CalSim modeling Scenario, made up of multiple model runs with the same
    Assumptions. One Scenario can have multiple model Runs to allow for
    improvements and bug fixes over time.
    """

    id: int | None = Field(default=None, repr=False)
    name: str
    assumptions: dict[str, str] = Field(repr=False)

    @classmethod
    def get_non_assumption_attrs(cls) -> tuple[str]:
        return ("id", "name")

    def get_assumption_attrs(self) -> tuple[str]:
        return tuple(self.assumptions.keys())


class Run(CSRS_Model):
    """A CalSim model run belonging to one Scenario. A model Run can contain
    many timeseries, and many metrics.
    """

    id: int | None = Field(default=None, repr=False)
    scenario: str
    version: str
    # info
    parent: str | None = Field(default=None, repr=False)
    children: tuple[str, ...] | tuple = Field(default_factory=tuple, repr=False)
    contact: str = Field(repr=False)
    confidential: bool = Field(default=False, repr=False)
    published: bool = Field(default=False, repr=False)
    code_version: str = Field(repr=False)
    detail: str = Field(repr=False)


class Timeseries(CSRS_Model):
    """The timeseries data belonging to one model Run."""

    scenario: str
    version: str
    # shadow pandss RegularTimeseries attributes
    path: str
    values: tuple[float, ...] = Field(default_factory=tuple, repr=False)
    dates: tuple[str, ...] = Field(default_factory=tuple, repr=False)
    period_type: str = Field(repr=False)
    units: str = Field(repr=False)
    interval: str = Field(repr=False)

    def to_pandss(self) -> "pdss.RegularTimeseries":
        import pandss as pdss

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
        rts: "pdss.RegularTimeseries",
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


class NamedPath(CSRS_Model):
    """A single DSS path, with information about the data it represents."""

    id: int | None = Field(default=None, repr=False)
    name: str
    path: str
    category: str = Field(repr=False)
    detail: str = Field(repr=False)
    period_type: str = Field(repr=False)
    interval: str = Field(repr=False)
    units: str = Field(repr=False)


class Metric(CSRS_Model):
    """An method of aggregation of timeseries data."""

    id: int | None = Field(default=None, repr=False)
    name: str
    index_detail: str = Field(repr=False)
    detail: str = Field(repr=False)


class MetricValue(CSRS_Model):
    """Aggregated values of timeseries data."""

    id: int | None = Field(default=None, repr=False)
    metric: str
    scenario: str
    run_version: str = Field(repr=False)
    path: str
    indexes: tuple = Field(default_factory=tuple, repr=False)
    values: tuple[float, ...] = Field(default_factory=tuple, repr=False)
