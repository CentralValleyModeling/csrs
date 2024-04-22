from sqlalchemy.orm import DeclarativeBase

from calsim_scenario_server import models as m
from calsim_scenario_server.enums import (
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
}

EXPECTED_PREFERRED_VERSIONS = {
    "scenario_id": int,
    "run_id": int,
}

EXPECTED_RUN_HISTORY = {
    "id": int,
    "run_id": int,
    "scenario_id": int,
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


def test_model_columns_assumption():
    check_model_columns(m.Assumption, EXPECTED_ASSUMPTION)


def test_model_column_types_assumption():
    check_model_column_types(m.Assumption, EXPECTED_ASSUMPTION)


def test_model_columns_metric_value():
    check_model_columns(m.MetricValue, EXPECTED_METRIC_VALUES)


def test_model_column_types_metric_value():
    check_model_column_types(m.MetricValue, EXPECTED_METRIC_VALUES)


def test_model_columns_metric():
    check_model_columns(m.Metric, EXPECTED_METRIC)


def test_model_column_types_metric():
    check_model_column_types(m.Metric, EXPECTED_METRIC)


def test_model_columns_path():
    check_model_columns(m.NamedPath, EXPECTED_PATH)


def test_model_column_types_path():
    check_model_column_types(m.NamedPath, EXPECTED_PATH)


def test_model_columns_run():
    check_model_columns(m.Run, EXPECTED_RUN)


def test_model_column_types_run():
    check_model_column_types(m.Run, EXPECTED_RUN)


def test_model_columns_run_history():
    check_model_columns(m.RunHistory, EXPECTED_RUN_HISTORY)


def test_model_column_types_run_history():
    check_model_column_types(m.RunHistory, EXPECTED_RUN_HISTORY)


def test_model_columns_scenario_assumptions():
    check_model_columns(m.ScenarioAssumptions, EXPECTED_SCENARIO_ASSUMPTIONS)


def test_model_column_types_scenario_assumptions():
    check_model_column_types(m.ScenarioAssumptions, EXPECTED_SCENARIO_ASSUMPTIONS)


def test_model_columns_scenario():
    check_model_columns(m.Scenario, EXPECTED_SCENARIO)


def test_model_column_types_scenario():
    check_model_column_types(m.Scenario, EXPECTED_SCENARIO)


def test_model_columns_preferred_versions():
    check_model_columns(m.PreferredVersion, EXPECTED_PREFERRED_VERSIONS)


def test_model_column_types_preferred_versions():
    check_model_column_types(m.PreferredVersion, EXPECTED_PREFERRED_VERSIONS)


def test_model_columns_unit():
    check_model_columns(m.Unit, EXPECTED_UNIT)


def test_model_column_types_unit():
    check_model_column_types(m.Unit, EXPECTED_UNIT)
