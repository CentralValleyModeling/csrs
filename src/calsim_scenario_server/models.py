from sqlalchemy import Boolean, Float, ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint


# Create a base class for our ORM models
class Base(DeclarativeBase):
    pass


# Define ORM models for each table
class Run(Base):
    __tablename__ = "runs"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = mapped_column(String, index=True)
    scenario_id = mapped_column(ForeignKey("scenarios.id"))
    version = mapped_column(String, nullable=False)

    scenario: Mapped["Scenario"] = relationship(back_populates="runs")


class RunMetadata(Base):
    __tablename__ = "run_metadata"

    run_id = mapped_column(
        ForeignKey("runs.id"),
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    predecessor_run_id = mapped_column(Integer, nullable=True)
    contact = mapped_column(String, nullable=False)
    confidential = mapped_column(Boolean, nullable=False)
    published = mapped_column(Boolean, nullable=False)
    code_version = mapped_column(String, nullable=False)
    detail = mapped_column(String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["run_id"], ["runs.id"]),
        ForeignKeyConstraint(["predecessor_run_id"], ["runs.id"]),
    )


class Scenario(Base):
    __tablename__ = "scenarios"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = mapped_column(String, nullable=False, unique=True)
    land_use_id = mapped_column(ForeignKey("land_use.id"), nullable=False)
    sea_level_rise_id = mapped_column(ForeignKey("sea_level_rise.id"), nullable=False)
    hydrology_id = mapped_column(ForeignKey("hydrology.id"), nullable=False)
    tucp_id = mapped_column(ForeignKey("tucp.id"), nullable=False)
    dcp_id = mapped_column(ForeignKey("dcp.id"), nullable=False)
    va_id = mapped_column(ForeignKey("va.id"), nullable=False)
    south_of_delta_id = mapped_column(ForeignKey("sod.id"), nullable=False)

    runs: Mapped[list["Run"]] = relationship(back_populates="scenario")


class Path(Base):
    __tablename__ = "paths"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = mapped_column(String)
    path = mapped_column(String)
    category = mapped_column(String)
    detail = mapped_column(String, nullable=False)

    __table_args__ = (UniqueConstraint("path", "category", name="unique_purpose"),)


class Metric(Base):
    __tablename__ = "metrics"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    index_detail = mapped_column(String, nullable=False)
    detail = mapped_column(String, nullable=False)


class TimeSeriesValue(Base):
    __tablename__ = "time_series_values"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id = mapped_column(ForeignKey("runs.id"))
    path_id = mapped_column(ForeignKey("paths.id"))
    timestep_id = mapped_column(ForeignKey("timesteps.id"))
    value = mapped_column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("run_id", "path_id", "timestep_id", name="unique_in_run"),
    )


class MetricValue(Base):
    __tablename__ = "metric_values"
    path_id = mapped_column(ForeignKey("paths.id"), primary_key=True)
    run_id = mapped_column(ForeignKey("runs.id"), primary_key=True)
    metric_id = mapped_column(ForeignKey("metrics.id"), primary_key=True)
    index = mapped_column(Integer, nullable=False)
    value = mapped_column(Float, nullable=False)


class TimeStep(Base):
    __tablename__ = "timesteps"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    datetime_str = mapped_column(String, nullable=False, unique=True)


class AssumptionLandUse(Base):
    __tablename__ = "land_use"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String, unique=True)
    future_year = mapped_column(Integer, nullable=False)


class AssumptionSeaLevelRise(Base):
    __tablename__ = "sea_level_rise"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String, unique=True, nullable=False)
    centimeters = mapped_column(Float, nullable=False)


class AssumptionHydrology(Base):
    __tablename__ = "hydrology"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String, unique=True, nullable=False)


class AssumptionTUCP(Base):
    __tablename__ = "tucp"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String, unique=True, nullable=False)


class AssumptionDeltaConveyanceProject(Base):
    __tablename__ = "dcp"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String, unique=True, nullable=False)


class AssumptionVoluntaryAgreements(Base):
    __tablename__ = "va"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String, unique=True, nullable=False)


class AssumptionSouthOfDeltaStorage(Base):
    __tablename__ = "sod"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String, unique=True, nullable=False)
