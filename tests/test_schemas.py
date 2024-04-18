import pandss as pdss

from calsim_scenario_server import schemas

EXPECTED_ASSUMPTION = {
    "id": int | None,
    "name": str,
    "kind": str,
    "detail": str,
}

EXPECTED_SCENARIO = {
    "id": int | None,
    "name": str,
    "version": str | None,
    "land_use": str,
    "sea_level_rise": str,
    "hydrology": str,
    "tucp": str,
    "dcp": str,
    "va": str,
    "south_of_delta": str,
}

EXPECTED_RUN = {
    "id": int | None,
    "scenario": str,
    "version": str,
    "parent": str | None,
    "children": tuple[str, ...] | tuple,
    "contact": str,
    "confidential": bool,
    "published": bool,
    "code_version": str,
    "detail": str,
}

EXPECTED_TIMESERIES = {
    "scenario": str,
    "version": str,
    "path": str | pdss.DatasetPath,
    "values": tuple[float, ...],
    "dates": tuple[str, ...],
    "period_type": str,
    "units": str,
    "interval": str,
}

EXPECTED_PATH = {
    "id": int | None,
    "name": str,
    "path": str,
    "category": str,
    "detail": str,
}

EXPECTED_METRIC = {
    "id": int | None,
    "name": str,
    "index_detail": str,
    "detail": str,
}

EXPECTED_METRIC_VALUES = {
    "id": int | None,
    "scenario": str,
    "run_version": str,
    "path": str,
    "metric": str,
    "indexes": tuple,
    "values": tuple[float, ...],
}


def check_schema_columns(schema: schemas.BaseModel, expectations: dict[str, type]):
    missing = list()
    for name in expectations:
        if name not in schema.model_fields:
            missing.append(name)
    assert len(missing) == 0, f"schema is missing expected columns: {missing}"
    extra = list()
    for name in schema.model_fields:
        if name not in expectations:
            extra.append(name)
    assert len(extra) == 0, f"model has unexpected columns: {extra}"


def check_schema_column_types(schema: schemas.BaseModel, expectations: dict[str, type]):
    columns = {name: info.annotation for name, info in schema.model_fields.items()}
    bad_types = list()
    for c in expectations:
        if columns[c] != expectations[c]:
            bad_types.append((c, columns[c], expectations[c]))
    assert len(bad_types) == 0, f"bad types: {bad_types}"


def test_schema_assumpiton_columns():
    check_schema_columns(schemas.Assumption, EXPECTED_ASSUMPTION)


def test_schema_assumpiton_column_types():
    check_schema_column_types(schemas.Assumption, EXPECTED_ASSUMPTION)


def test_schema_metric_value_columns():
    check_schema_columns(schemas.MetricValue, EXPECTED_METRIC_VALUES)


def test_schema_metric_value_column_types():
    check_schema_column_types(schemas.MetricValue, EXPECTED_METRIC_VALUES)


def test_schema_metric_columns():
    check_schema_columns(schemas.Metric, EXPECTED_METRIC)


def test_schema_metric_column_types():
    check_schema_column_types(schemas.Metric, EXPECTED_METRIC)


def test_schema_path_columns():
    check_schema_columns(schemas.NamedDatasetPath, EXPECTED_PATH)


def test_schema_path_column_types():
    check_schema_column_types(schemas.NamedDatasetPath, EXPECTED_PATH)


def test_schema_run_columns():
    check_schema_columns(schemas.Run, EXPECTED_RUN)


def test_schema_run_column_types():
    check_schema_column_types(schemas.Run, EXPECTED_RUN)


def test_schema_scenario_columns():
    check_schema_columns(schemas.Scenario, EXPECTED_SCENARIO)


def test_schema_scenario_column_types():
    check_schema_column_types(schemas.Scenario, EXPECTED_SCENARIO)


def test_schema_timeseries_columns():
    check_schema_columns(schemas.Timeseries, EXPECTED_TIMESERIES)


def test_schema_timeseries_column_types():
    check_schema_column_types(schemas.Timeseries, EXPECTED_TIMESERIES)
