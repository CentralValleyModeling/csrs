from typing import Optional

from sqlalchemy import Enum as sqlalchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from .enum import AssumptionEnum, DimensionalityEnum, PathCategoryEnum


# Create a base class for our ORM models
class Base(DeclarativeBase):
    pass


# Define ORM models for each table
class RunModel(Base):
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
    # Multi-column unique rules
    __table_args__ = (
        UniqueConstraint(
            "scenario_id",
            "version",
            name="unique_purpose",
        ),
    )


class ScenarioModel(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    # ORM relationships
    runs: Mapped[list[RunModel]] = relationship(back_populates="scenario")
    assumption_maps: Mapped[list["ScenarioAssumptionsModel"]] = relationship(
        back_populates="scenario"
    )


class ScenarioAssumptionsModel(Base):
    __tablename__ = "scenario_assumptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"), nullable=False)
    assumption_kind: Mapped[AssumptionEnum] = mapped_column(nullable=False)
    assumption_id: Mapped[int] = mapped_column(
        ForeignKey("assumptions.id"), nullable=False
    )
    # ORM relationships
    scenario: Mapped[ScenarioModel] = relationship(back_populates="assumption_maps")
    assumption: Mapped["AssumptionModel"] = relationship(back_populates="scenario_map")


class NamedPathModel(Base):
    __tablename__ = "paths"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = mapped_column(String)
    path = mapped_column(String)
    category = mapped_column(sqlalchemyEnum(PathCategoryEnum), nullable=False)
    detail = mapped_column(String, nullable=False)
    # Multi-column unique rules
    __table_args__ = (UniqueConstraint("path", "category", name="unique_purpose"),)


class UnitModel(Base):
    __tablename__ = "units"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = mapped_column(String, unique=True)
    dimensionality = mapped_column(sqlalchemyEnum(DimensionalityEnum), nullable=False)


class MetricModel(Base):
    __tablename__ = "metrics"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = mapped_column(String, unique=True)
    index_detail = mapped_column(String, nullable=False)
    detail = mapped_column(String, nullable=False)


class TimeSeriesModel(Base):
    __tablename__ = "time_series_values"

    run_id = mapped_column(ForeignKey("runs.id"), primary_key=True)
    path_id = mapped_column(ForeignKey("paths.id"), primary_key=True)
    timestep_id = mapped_column(ForeignKey("timesteps.id"), primary_key=True)
    units = mapped_column(ForeignKey("units.id"))
    value = mapped_column(Float, nullable=False)
    # Multi-column unique rules
    __table_args__ = (
        UniqueConstraint(
            "run_id",
            "path_id",
            "timestep_id",
            name="unique_in_run",
        ),
    )


class MetricValueModel(Base):
    __tablename__ = "metric_values"

    path_id = mapped_column(ForeignKey("paths.id"), primary_key=True)
    run_id = mapped_column(ForeignKey("runs.id"), primary_key=True)
    metric_id = mapped_column(ForeignKey("metrics.id"), primary_key=True)
    index = mapped_column(Integer, nullable=False)
    units = mapped_column(ForeignKey("units.name"))
    value = mapped_column(Float, nullable=False)


class TimestepModel(Base):
    __tablename__ = "timesteps"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    datetime_str = mapped_column(String, nullable=False, unique=True)


class AssumptionModel(Base):
    __tablename__ = "assumptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    kind: Mapped[AssumptionEnum] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column()
    # ORM relationships
    scenario_map: Mapped[list[ScenarioAssumptionsModel]] = relationship(
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
