from sqlalchemy.orm import DeclarativeBase

from calsim_scenario_server import models as m
from calsim_scenario_server.enum import (
    AssumptionEnum,
    DimensionalityEnum,
    PathCategoryEnum,
)

EXPECTED_ASSUMPTION = {
    "id": int,
    "name": str,
    "kind": AssumptionEnum,
    "detail": str,
}

EXPECTED_METRIC_VALUES = {
    "path_id": int,
    "run_id": int,
    "metric_id": int,
    "index": int,
    "units": str,
    "value": float,
}

EXPECTED_METRIC = {
    "id": int,
    "name": str,
    "index_detail": str,
    "detail": str,
}

EXPECTED_PATH = {
    "id": int,
    "name": str,
    "path": str,
    "category": PathCategoryEnum,
    "detail": str,
}

EXPECTED_RUN = {
    "id": int,
    "parent_id": int,
    "scenario_id": int,
    "version": str,
    "contact": str,
    "confidential": bool,
    "published": bool,
    "code_version": str,
    "detail": str,
    "dss": str,
}

EXPECTED_SCENARIO_ASSUMPTIONS = {
    "id": int,
    "scenario_id": int,
    "assumption_kind": AssumptionEnum,
    "assumption_id": int,
}

EXPECTED_SCENARIO = {
    "id": int,
    "name": str,
    "version": str,
}

EXPECTED_UNIT = {
    "id": int,
    "name": str,
    "dimensionality": DimensionalityEnum,
}


def check_model_columns(model: DeclarativeBase, expectations: dict[str, type]):
    columns = [c.key for c in model.__table__.columns]
    missing = list()
    for c in expectations:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in expectations:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def check_model_column_types(model: DeclarativeBase, expectations: dict[str, type]):
    columns = {c.key: c.type.python_type for c in model.__table__.columns}
    bad_types = list()
    for c in expectations:
        if columns[c] != expectations[c]:
            bad_types.append((c, columns[c], expectations[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_assumption_model_columns():
    check_model_columns(m.AssumptionModel, EXPECTED_ASSUMPTION)


def test_assumption_model_column_types():
    check_model_column_types(m.AssumptionModel, EXPECTED_ASSUMPTION)


def test_metric_value_model_columns():
    check_model_columns(m.MetricValueModel, EXPECTED_METRIC_VALUES)


def test_metric_value_model_column_types():
    check_model_column_types(m.MetricValueModel, EXPECTED_METRIC_VALUES)


def test_metric_model_columns():
    check_model_columns(m.MetricModel, EXPECTED_METRIC)


def test_metric_model_column_types():
    check_model_column_types(m.MetricModel, EXPECTED_METRIC)


def test_path_model_columns():
    check_model_columns(m.NamedPathModel, EXPECTED_PATH)


def test_path_model_column_types():
    check_model_column_types(m.NamedPathModel, EXPECTED_PATH)


def test_run_model_columns():
    check_model_columns(m.RunModel, EXPECTED_RUN)


def test_run_model_column_types():
    check_model_column_types(m.RunModel, EXPECTED_RUN)


def test_scenario_assumptions_model_columns():
    check_model_columns(m.ScenarioAssumptionsModel, EXPECTED_SCENARIO_ASSUMPTIONS)


def test_scenario_assumptions_model_column_types():
    check_model_column_types(m.ScenarioAssumptionsModel, EXPECTED_SCENARIO_ASSUMPTIONS)


def test_scenario_model_columns():
    check_model_columns(m.ScenarioModel, EXPECTED_SCENARIO)


def test_scenario_model_column_types():
    check_model_column_types(m.ScenarioModel, EXPECTED_SCENARIO)


def test_unit_model_columns():
    check_model_columns(m.UnitModel, EXPECTED_UNIT)


def test_unit_model_column_types():
    check_model_column_types(m.UnitModel, EXPECTED_UNIT)
