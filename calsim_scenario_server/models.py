"""SQL models for the CalSim Scenario Server"""

from typing import Optional

from sqlalchemy import Enum as sqlalchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from .enum import AssumptionEnum, DimensionalityEnum, PathCategoryEnum


# Create a base class for our ORM models
class Base(DeclarativeBase):
    pass


class AssumptionModel(Base):
    """Data regarding single modeling assumptions."""

    __tablename__ = "assumptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    kind: Mapped[AssumptionEnum] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column()
    # ORM relationships
    scenario_map: Mapped[list["ScenarioAssumptionsModel"]] = relationship(
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


class ScenarioAssumptionsModel(Base):
    """Data regarding which modeling scenarios use which assumptions."""

    __tablename__ = "scenario_assumptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"), nullable=False)
    assumption_kind: Mapped[AssumptionEnum] = mapped_column(nullable=False)
    assumption_id: Mapped[int] = mapped_column(
        ForeignKey("assumptions.id"), nullable=False
    )
    # ORM relationships
    scenario: Mapped["ScenarioModel"] = relationship(back_populates="assumption_maps")
    assumption: Mapped["AssumptionModel"] = relationship(back_populates="scenario_map")


class ScenarioModel(Base):
    """Data establishing modeling scenarios."""

    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    # ORM relationships
    runs: Mapped[list["RunModel"]] = relationship(back_populates="scenario")
    assumption_maps: Mapped[list["ScenarioAssumptionsModel"]] = relationship(
        back_populates="scenario"
    )


# Define ORM models for each table
class RunModel(Base):
    """Data and metadata establishing model runs."""

    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("runs.id"))
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"))
    version: Mapped[str] = mapped_column(nullable=False)
    # metadata
    contact: Mapped[str] = mapped_column(nullable=False)
    confidential: Mapped[bool] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(nullable=False)
    code_version: Mapped[str] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column(nullable=False)
    # ORM relationships
    scenario: Mapped["ScenarioModel"] = relationship(back_populates="runs")
    children: Mapped[list["RunModel"]] = relationship(back_populates="parent")
    parent: Mapped["RunModel"] = relationship(
        back_populates="children",
        remote_side=[id],
    )
    dss_lookup: Mapped["DSSLookup"] = relationship(back_populates="run")
    # Multi-column unique rules
    __table_args__ = (
        UniqueConstraint(
            "scenario_id",
            "version",
            name="unique_purpose",
        ),
    )


class DSSLookup(Base):
    """Data about the DSS file used to store timeseries data for a run."""

    __tablename__ = "dss_lookup"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"), nullable=False)
    source: Mapped[str] = mapped_column(nullable=False)
    # ORM relationships
    run: Mapped["RunModel"] = relationship(back_populates="dss_lookup")
    catalog: Mapped[list["CommonCatalog"]] = relationship(back_populates="dss_lookup")


class CommonCatalog(Base):
    """Data about the paths contained in each DSS file."""

    __tablename__ = "common_catalog"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("dss_lookup.id"), nullable=False)
    path_id: Mapped[int] = mapped_column(ForeignKey("paths.id"), nullable=False)
    # ORM relationships
    dss_lookup: Mapped["DSSLookup"] = relationship(back_populates="catalog")
    path: Mapped["NamedPathModel"] = relationship()


class NamedPathModel(Base):
    """Data about the meaning and A-F representation of DSS Paths."""

    __tablename__ = "paths"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()
    category: Mapped[PathCategoryEnum] = mapped_column(
        sqlalchemyEnum(PathCategoryEnum), nullable=False
    )
    detail: Mapped[str] = mapped_column(nullable=False)
    # Multi-column unique rules
    __table_args__ = (UniqueConstraint("path", "category", name="unique_purpose"),)


class UnitModel(Base):
    """Data about the units used by timeseries and metrics."""

    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    dimensionality: Mapped[DimensionalityEnum] = mapped_column(
        sqlalchemyEnum(DimensionalityEnum), nullable=False
    )


class MetricModel(Base):
    """Data about the meaning of metrics."""

    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    index_detail: Mapped[str] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column(nullable=False)


class MetricValueModel(Base):
    """Data for the processed metrics."""

    __tablename__ = "metric_values"

    path_id: Mapped[int] = mapped_column(ForeignKey("paths.id"), primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"), primary_key=True)
    metric_id: Mapped[int] = mapped_column(ForeignKey("metrics.id"), primary_key=True)
    index: Mapped[int] = mapped_column(nullable=False)
    units: Mapped[str] = mapped_column(ForeignKey("units.name"))
    value: Mapped[float] = mapped_column(nullable=False)
