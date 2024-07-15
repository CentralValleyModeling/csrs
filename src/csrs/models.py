"""SQL models for the CalSim Scenario Server"""

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from .enums import IntervalEnum, PeriodTypeEnum


# Create a base class for our ORM models
class Base(DeclarativeBase):
    pass


class Assumption(Base):
    """Data regarding single modeling assumptions."""

    __tablename__ = "assumptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    kind: Mapped[str] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column()
    # ORM relationships
    scenario_map: Mapped[list["ScenarioAssumptions"]] = relationship(
        back_populates="assumption"
    )
    # Multi-column unique rules
    __table_args__ = (
        UniqueConstraint(
            "name",
            "kind",
            name="unique_name",
        ),
        UniqueConstraint(
            "detail",
            "kind",
            name="unique_detail",
        ),
    )


class ScenarioAssumptions(Base):
    """Data regarding which modeling scenarios use which assumptions."""

    __tablename__ = "scenario_assumptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"), nullable=False)
    assumption_kind: Mapped[str] = mapped_column(nullable=False)
    assumption_id: Mapped[int] = mapped_column(
        ForeignKey("assumptions.id"), nullable=False
    )
    # ORM relationships
    scenario: Mapped["Scenario"] = relationship(back_populates="assumption_maps")
    assumption: Mapped["Assumption"] = relationship(back_populates="scenario_map")


class Scenario(Base):
    """Data establishing modeling scenarios."""

    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    # ORM relationships
    history: Mapped[list["RunHistory"]] = relationship(viewonly=True)
    preference: Mapped["PreferredVersion"] = relationship(back_populates="scenario")
    assumption_maps: Mapped[list["ScenarioAssumptions"]] = relationship(
        back_populates="scenario"
    )

    @property
    def version(self) -> str:
        if self.run:
            return self.run.version
        return None

    @property
    def versions(self) -> list[str]:
        return [r.version for r in self.history]

    @property
    def run(self) -> "Run":
        if self.preference:
            return self.preference.run
        return None


class Run(Base):
    """Data and metadata establishing model runs."""

    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"))
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("runs.id"),
        nullable=True,
    )
    # metadata
    contact: Mapped[str] = mapped_column(nullable=False)
    confidential: Mapped[bool] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(nullable=False)
    code_version: Mapped[str] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column(nullable=False)
    # ORM relationships
    history: Mapped["RunHistory"] = relationship(back_populates="run")
    prefered_via: Mapped["PreferredVersion"] = relationship(back_populates="run")
    scenario: Mapped["Scenario"] = relationship(viewonly=True)
    children: Mapped[list["Run"]] = relationship(back_populates="parent")
    parent: Mapped["Run"] = relationship(
        back_populates="children",
        remote_side=[id],
    )
    catalog: Mapped[list["CommonCatalog"]] = relationship(back_populates="run")

    @property
    def version(self) -> str:
        return self.history.version


class PreferredVersion(Base):
    """Data relating the Scenario to it's current preferred Run."""

    __tablename__ = "preferred_versions"

    scenario_id: Mapped[int] = mapped_column(
        ForeignKey("scenarios.id"),
        primary_key=True,
        nullable=False,
    )
    run_id: Mapped[int] = mapped_column(
        ForeignKey("runs.id"),
        nullable=False,
    )
    # ORM relationships
    scenario: Mapped["Scenario"] = relationship(back_populates="preference")
    run: Mapped["Run"] = relationship(back_populates="prefered_via")
    # Multi-column unique rules
    __table_args__ = (
        UniqueConstraint(
            "scenario_id",
            "run_id",
            name="unique_preference",
        ),
    )

    @property
    def history(self) -> "RunHistory":
        return self.run.history

    @property
    def version(self) -> str:
        return self.history.version


class RunHistory(Base):
    """Data relating the Scenario to it's Run history."""

    __tablename__ = "run_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id = mapped_column(ForeignKey("runs.id"), nullable=False)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"))
    version: Mapped[str] = mapped_column(nullable=False)
    # ORM relationships
    scenario: Mapped["Scenario"] = relationship(viewonly=True)
    run: Mapped["Run"] = relationship(back_populates="history")
    # Multi-column unique rules
    __table_args__ = (
        UniqueConstraint(
            "scenario_id",
            "run_id",
            name="unique_run",
        ),
        UniqueConstraint(
            "scenario_id",
            "version",
            name="unique_version",
        ),
    )


class CommonCatalog(Base):
    """Data about the paths contained in each DSS file."""

    __tablename__ = "common_catalog"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"), nullable=False)
    path_id: Mapped[int] = mapped_column(ForeignKey("named_paths.id"), nullable=False)
    # ORM relationships
    path: Mapped["NamedPath"] = relationship()
    run: Mapped["Run"] = relationship(back_populates="catalog")


class NamedPath(Base):
    """Data about the meaning and A-F representation of DSS Paths."""

    __tablename__ = "named_paths"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column(nullable=False)
    period_type: Mapped[PeriodTypeEnum] = mapped_column(nullable=False)
    interval: Mapped[IntervalEnum] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column(nullable=False)
    units: Mapped[str] = mapped_column(nullable=False)
    # Multi-column unique rules
    __table_args__ = (UniqueConstraint("name", "category", name="unique_purpose"),)


class TimeseriesLedger(Base):
    """Long ledger of timeseries data."""

    __tablename__ = "timeseries_ledger"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"), nullable=False)
    path_id: Mapped[int] = mapped_column(ForeignKey("named_paths.id"), nullable=False)
    datetime: Mapped[float] = mapped_column(nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
    # Multi-column unique rules
    __table_args__ = (
        UniqueConstraint(
            "run_id",
            "path_id",
            "datetime",
            name="unique_datapoint",
        ),
    )


class Metric(Base):
    """Data about the meaning of metrics."""

    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    index_detail: Mapped[str] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column(nullable=False)


class MetricValue(Base):
    """Data for the processed metrics."""

    __tablename__ = "metric_values"

    path_id: Mapped[int] = mapped_column(ForeignKey("named_paths.id"), primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"), primary_key=True)
    metric_id: Mapped[int] = mapped_column(ForeignKey("metrics.id"), primary_key=True)
    index: Mapped[int] = mapped_column(nullable=False)
    units: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
