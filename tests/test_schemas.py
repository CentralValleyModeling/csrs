import pandas as pd
import pandss as pdss

from csrs import schemas

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
    "path": str,
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


def test_schema_columns_assumpiton():
    check_schema_columns(schemas.Assumption, EXPECTED_ASSUMPTION)


def test_schema_column_types_assumpiton():
    check_schema_column_types(schemas.Assumption, EXPECTED_ASSUMPTION)


def test_schema_columns_metric_value():
    check_schema_columns(schemas.MetricValue, EXPECTED_METRIC_VALUES)


def test_schema_column_types_metric_value():
    check_schema_column_types(schemas.MetricValue, EXPECTED_METRIC_VALUES)


def test_schema_columns_metric():
    check_schema_columns(schemas.Metric, EXPECTED_METRIC)


def test_schema_column_types_metric():
    check_schema_column_types(schemas.Metric, EXPECTED_METRIC)


def test_schema_columns_path():
    check_schema_columns(schemas.NamedDatasetPath, EXPECTED_PATH)


def test_schema_column_types_path():
    check_schema_column_types(schemas.NamedDatasetPath, EXPECTED_PATH)


def test_schema_columns_run():
    check_schema_columns(schemas.Run, EXPECTED_RUN)


def test_schema_column_types_run():
    check_schema_column_types(schemas.Run, EXPECTED_RUN)


def test_schema_columns_scenario():
    check_schema_columns(schemas.Scenario, EXPECTED_SCENARIO)


def test_schema_column_types_scenario():
    check_schema_column_types(schemas.Scenario, EXPECTED_SCENARIO)


def test_schema_columns_timeseries():
    check_schema_columns(schemas.Timeseries, EXPECTED_TIMESERIES)


def test_schema_column_types_timeseries():
    check_schema_column_types(schemas.Timeseries, EXPECTED_TIMESERIES)


def test_schema_conversion_timeseries():
    ts = schemas.Timeseries(
        scenario="test-schema-conversion-timeseries",
        version="0.1",
        path=str(pdss.DatasetPath(b="TEST", c="TESTING")),
        values=(1.0, 2.0, 3.0),
        dates=("2024-01-31", "2024-02-29", "2024-03-30"),
        period_type="PER-CUM",
        units="TAF",
        interval="1MON",
    )
    rts = ts.to_pandss()

    assert isinstance(rts, pdss.RegularTimeseries)

    ts2 = schemas.Timeseries.from_pandss(
        scenario=ts.scenario,
        version=ts.version,
        rts=rts,
    )

    assert isinstance(ts2, schemas.Timeseries)

    assert ts.interval == ts2.interval  # Check an attr that pandss mutates
    for L, R in zip(ts.dates, ts2.dates):  # Check an array of values
        assert L == R


def test_schema_conversion_dataframe():
    ts = schemas.Timeseries(
        scenario="test-schema-conversion-timeseries",
        version="0.1",
        path=str(pdss.DatasetPath(b="TEST", c="TESTING")),
        values=(1.0, 2.0, 3.0),
        dates=("2024-01-31", "2024-02-29", "2024-03-30"),
        period_type="PER-CUM",
        units="TAF",
        interval="1MON",
    )
    df = ts.to_frame()
    assert isinstance(df, pd.DataFrame)
    assert "SCENARIO" in df.columns.names
    assert ts.version == df.columns.to_frame()["VERSION"].iat[0]
