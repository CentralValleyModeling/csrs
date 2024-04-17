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
    "code_version": bool,
    "detail": bool,
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


def test_assumption_model_columns():
    columns = [c.key for c in m.AssumptionModel.__table__.columns]
    missing = list()
    for c in EXPECTED_ASSUMPTION:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in EXPECTED_ASSUMPTION:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def test_assumption_model_column_types():
    columns = {c.key: c.type.python_type for c in m.AssumptionModel.__table__.columns}
    bad_types = list()
    for c in EXPECTED_ASSUMPTION:
        if EXPECTED_ASSUMPTION[c] != EXPECTED_ASSUMPTION[c]:
            bad_types.append((c, columns[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_metric_value_model_columns():
    columns = [c.key for c in m.MetricValueModel.__table__.columns]
    missing = list()
    for c in EXPECTED_METRIC_VALUES:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in EXPECTED_METRIC_VALUES:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def test_metric_value_model_column_types():
    columns = {c.key: c.type.python_type for c in m.MetricValueModel.__table__.columns}
    bad_types = list()
    for c in EXPECTED_METRIC_VALUES:
        if EXPECTED_METRIC_VALUES[c] != EXPECTED_METRIC_VALUES[c]:
            bad_types.append((c, columns[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_metric_model_columns():
    columns = [c.key for c in m.MetricModel.__table__.columns]
    missing = list()
    for c in EXPECTED_METRIC:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in EXPECTED_METRIC:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def test_metric_model_column_types():
    columns = {c.key: c.type.python_type for c in m.MetricModel.__table__.columns}
    bad_types = list()
    for c in EXPECTED_METRIC:
        if EXPECTED_METRIC[c] != EXPECTED_METRIC[c]:
            bad_types.append((c, columns[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_path_model_columns():
    columns = [c.key for c in m.NamedPathModel.__table__.columns]
    missing = list()
    for c in EXPECTED_PATH:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in EXPECTED_PATH:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def test_path_model_column_types():
    columns = {c.key: c.type.python_type for c in m.NamedPathModel.__table__.columns}
    bad_types = list()
    for c in EXPECTED_PATH:
        if EXPECTED_PATH[c] != EXPECTED_PATH[c]:
            bad_types.append((c, columns[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_run_model_columns():
    columns = [c.key for c in m.RunModel.__table__.columns]
    missing = list()
    for c in EXPECTED_RUN:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in EXPECTED_RUN:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def test_run_model_column_types():
    columns = {c.key: c.type.python_type for c in m.RunModel.__table__.columns}
    bad_types = list()
    for c in EXPECTED_RUN:
        if EXPECTED_RUN[c] != EXPECTED_RUN[c]:
            bad_types.append((c, columns[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_scenario_assumptions_model_columns():
    columns = [c.key for c in m.ScenarioAssumptionsModel.__table__.columns]
    missing = list()
    for c in EXPECTED_SCENARIO_ASSUMPTIONS:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in EXPECTED_SCENARIO_ASSUMPTIONS:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def test_scenario_assumptions_model_column_types():
    columns = {
        c.key: c.type.python_type for c in m.ScenarioAssumptionsModel.__table__.columns
    }
    bad_types = list()
    for c in EXPECTED_SCENARIO_ASSUMPTIONS:
        if EXPECTED_SCENARIO_ASSUMPTIONS[c] != EXPECTED_SCENARIO_ASSUMPTIONS[c]:
            bad_types.append((c, columns[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_scenario_model_columns():
    columns = [c.key for c in m.ScenarioModel.__table__.columns]
    missing = list()
    for c in EXPECTED_SCENARIO:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in EXPECTED_SCENARIO:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def test_scenario_model_column_types():
    columns = {c.key: c.type.python_type for c in m.ScenarioModel.__table__.columns}
    bad_types = list()
    for c in EXPECTED_SCENARIO:
        if EXPECTED_SCENARIO[c] != EXPECTED_SCENARIO[c]:
            bad_types.append((c, columns[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_unit_model_columns():
    columns = [c.key for c in m.UnitModel.__table__.columns]
    missing = list()
    for c in EXPECTED_UNIT:
        if c not in columns:
            missing.append(c)
    assert len(missing) == 0, f"model is missing expected columns: {missing}"
    extra = list()
    for c in columns:
        if c not in EXPECTED_UNIT:
            extra.append(c)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def test_unit_model_column_types():
    columns = {c.key: c.type.python_type for c in m.UnitModel.__table__.columns}
    bad_types = list()
    for c in EXPECTED_UNIT:
        if EXPECTED_UNIT[c] != EXPECTED_UNIT[c]:
            bad_types.append((c, columns[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"
