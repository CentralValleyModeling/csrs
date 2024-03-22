from sqlalchemy import Boolean, Float, ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Create a base class for our ORM models
Base: DeclarativeMeta = declarative_base()


# Define ORM models for each table
class Run(Base):
    __tablename__ = "runs"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = mapped_column(String, index=True)
    scenario_id = mapped_column(ForeignKey("scenarios.id"))
    version = mapped_column(String)

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
    contact = mapped_column(String)
    confidential = mapped_column(Boolean)
    published = mapped_column(Boolean)
    code_version = mapped_column(String)
    detail = mapped_column(String)

    __table_args__ = (
        ForeignKeyConstraint(["run_id"], ["runs.id"]),
        ForeignKeyConstraint(["predecessor_run_id"], ["runs.id"]),
    )


class Scenario(Base):
    __tablename__ = "scenarios"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    scenario_name = mapped_column(String)
    land_use_id = mapped_column(ForeignKey("land_use.id"))
    sea_level_rise_id = mapped_column(ForeignKey("sea_level_rise.id"))
    hydrology_id = mapped_column(ForeignKey("hydrology.id"))
    tucp_id = mapped_column(ForeignKey("tucp.id"))
    dcp_id = mapped_column(ForeignKey("dcp.id"))
    va_id = mapped_column(ForeignKey("va.id"))
    sod_id = mapped_column(ForeignKey("sod.id"))

    runs: Mapped[list["Run"]] = relationship(back_populates="scenario")


class Path(Base):
    __tablename__ = "paths"

    path_id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    path = mapped_column(String)
    category = mapped_column(String)
    detail = mapped_column(String)


class Metric(Base):
    __tablename__ = "metrics"

    metric_id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    index_detail = mapped_column(String)
    detail = mapped_column(String)


class TimeSeriesValue(Base):
    __tablename__ = "time_series_values"

    run_id = mapped_column(ForeignKey("runs.id"), primary_key=True)
    path_id = mapped_column(ForeignKey("paths.path_id"), primary_key=True)
    dt_index = mapped_column(ForeignKey("timesteps.dt_index"))
    value = mapped_column(Float)


class MetricValue(Base):
    __tablename__ = "metric_values"

    path_id = mapped_column(ForeignKey("paths.path_id"), primary_key=True)
    run_id = mapped_column(ForeignKey("runs.id"), primary_key=True)
    metric_id = mapped_column(ForeignKey("metrics.metric_id"), primary_key=True)
    index = mapped_column(Integer)
    value = mapped_column(Float)


class TimeStep(Base):
    __tablename__ = "timesteps"

    dt_index = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    datetime_str = mapped_column(String)


class LandUse(Base):
    __tablename__ = "land_use"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String)
    future_year = mapped_column(Integer)


class SeaLevelRise(Base):
    __tablename__ = "sea_level_rise"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String)
    centimeters = mapped_column(Float)


class Hydrology(Base):
    __tablename__ = "hydrology"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String)


class TUCP(Base):
    __tablename__ = "tucp"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String)


class DCP(Base):
    __tablename__ = "dcp"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String)


class VA(Base):
    __tablename__ = "va"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String)


class SOD(Base):
    __tablename__ = "sod"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    detail = mapped_column(String)
