import sqlite3
from datetime import datetime
from os import remove
from pathlib import Path
from typing import Any


def seconds_since_1900():
    EPOCH = datetime(1900, 1, 1)
    current_date = datetime(1921, 10, 1)
    while True:
        # Calculate total seconds since base_date
        total_seconds = (current_date - EPOCH).total_seconds()
        yield total_seconds
        # Move to the next month
        year = current_date.year
        month = current_date.month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        # Calculate the next date
        current_date = datetime(year, month, 1)


def add_rows_to_table(
    cursor: sqlite3.Cursor,
    table_name: str,
    rows: list[dict[str, Any]],
):
    for item in rows:
        c_names = ", ".join(item.keys())
        v_names = ":" + ", :".join(item.keys())
        cursor.execute(
            f"INSERT INTO {table_name} ({c_names}) VALUES ({v_names});",
            item,
        )


def create_empty_database(dst: Path, raw_sql_file: Path) -> sqlite3.Connection:
    if dst.exists():
        remove(dst)
    connection = sqlite3.connect(dst)
    with open(raw_sql_file, "r") as RAW:
        sql = RAW.read()
    connection.executescript(sql)
    return connection


def add_assumption(cursor: sqlite3.Cursor):
    assumptions = [
        {
            "id": 1,
            "name": "testing-assumption-existing",
            "kind": "testing",
            "detail": "Used for testing the CSRS databse, existing assumption #1",
        },
    ]
    add_rows_to_table(cursor, "assumptions", assumptions)


def add_scenario(cursor: sqlite3.Cursor):
    scenarios = [
        {
            "id": 1,
            "name": "testing-scenario",
        }
    ]
    linked_assumptions = [
        {
            "scenario_id": 1,
            "assumption_kind": "testing",
            "assumption_id": 1,
        },
    ]

    add_rows_to_table(cursor, "scenarios", scenarios)
    add_rows_to_table(cursor, "scenario_assumptions", linked_assumptions)


def add_run(cursor: sqlite3.Cursor):
    runs = [
        {
            "scenario_id": 1,
            "contact": "run@testing.gov",
            "confidential": True,
            "published": False,
            "code_version": "0.0.0",
            "detail": "Used for testing the CSRS databse, existing run #1",
        }
    ]
    preferences = [
        {
            "scenario_id": 1,
            "run_id": 1,
        }
    ]
    history = [
        {
            "run_id": 1,
            "scenario_id": 1,
            "version": "1.0",
        }
    ]
    add_rows_to_table(cursor, "runs", runs)
    add_rows_to_table(cursor, "preferred_versions", preferences)
    add_rows_to_table(cursor, "run_history", history)


def add_path(cursor: sqlite3.Cursor):
    paths = [
        {
            "id": 1,
            "name": "testing-paths-existing",
            "path": "//TEST_PATH/TESTING//1MON//",
            "category": "testing",
            "period_type": "PER-AVER",
            "interval": "1MON",
            "detail": "Used for testing the CSRS databse, existing path #1",
            "units": "NONE",
        }
    ]
    catalog = [
        {
            "run_id": 1,
            "path_id": 1,
        }
    ]
    add_rows_to_table(cursor, "named_paths", paths)
    add_rows_to_table(cursor, "common_catalog", catalog)


def add_timeseries(cursor: sqlite3.Cursor):
    timeseries = [
        {
            "run_id": 1,
            "path_id": 1,
            "datetime": datetime,
            "value": value,
        }
        for datetime, value in zip(seconds_since_1900(), range(1, 101))
    ]
    add_rows_to_table(cursor, "timeseries_ledger", timeseries)


def add_metric(cursor: sqlite3.Cursor):
    metrics = [
        {
            "id": 1,
            "name": "testing-metric-existing",
            "x_detail": "A single item.",
            "detail": "Used for testing the CSRS databse, existing metric #1",
        }
    ]
    metric_values = [
        {
            "path_id": 1,
            "run_id": 1,
            "metric_id": 1,
            "x": 0,
            "units": "NONE",
            "value": 1.0,
        }
    ]
    add_rows_to_table(cursor, "metrics", metrics)
    add_rows_to_table(cursor, "metric_values", metric_values)


if __name__ == "__main__":
    here = Path(__file__).parent
    csrs_dir = here.parent.parent / "src/csrs"
    raw_sql_file = csrs_dir / "database_recipe.sql"
    database = here / "_testing.db"
    with create_empty_database(dst=database, raw_sql_file=raw_sql_file) as conn:
        cursor = conn.cursor()
        add_assumption(cursor)
        add_scenario(cursor)
        add_run(cursor)
        add_path(cursor)
        add_timeseries(cursor)
        add_metric(cursor)
