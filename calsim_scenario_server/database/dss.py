import json
import sqlite3
from pathlib import Path
from time import perf_counter
from typing import Iterator

import pandas as pd
import pandss as pdss

STANDARD_PATHS_FILE = Path(__file__).parent / "standard_paths.json"
with open(STANDARD_PATHS_FILE, "r") as src:
    d = json.load(src)
    STANDARD_PATHS = {name: pdss.DatasetPath(**kwargs) for name, kwargs in d.items()}


def read_paths(
    dss: pdss.DSS,
    paths: dict[str, pdss.DatasetPath],
    raise_error_on_empty: bool = False,
    raise_error_on_multiple: bool = True,
) -> Iterator[tuple[str, pdss.RegularTimeseries]]:
    with dss:
        for name, path in paths.items():
            datasets = list(dss.read_multiple_rts(path))
            if raise_error_on_empty and (len(datasets) < 1):
                raise ValueError(f"no datasets read for {path=}")
            elif raise_error_on_multiple and (len(datasets) > 1):
                raise ValueError(f"multiple datasets read for {path=}")

            if len(datasets) > 0:
                yield name, datasets[0]


def add_to_data_ledger(
    cursor: sqlite3.Cursor,
    run_id: int,
    dss: pdss.DSS,
    paths: dict[str, pdss.DatasetPath],
):
    df_paths = pd.read_sql_query("SELECT * FROM common_paths", con=cursor.connection)
    query = """
    INSERT INTO data_ledger
    (run_id, path_id, datetime, value)
    VALUES (?, ?, ?, ?)
    """
    for name, rts in read_paths(dss, paths):
        path_id = df_paths.loc[df_paths["name"] == name, "path_id"].iat[0]
        df = rts.to_frame()
        df.columns = ["value"]
        df.index.name = "datetime"
        df["run_id"] = run_id
        df["path_id"] = int(path_id)
        df.index = df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
        df = df.reset_index()[["run_id", "path_id", "datetime", "value"]]
        cursor.executemany(query, df.values)


def _temp_db_creation(dst: Path) -> sqlite3.Connection:
    dst = Path(dst)
    conn = sqlite3.connect(dst)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS data_ledger (
            run_id INTEGER,
            path_id INTEGER,
            datetime TEXT,
            value REAL
        );
        """
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS common_paths (
            path_id INTEGER,
            name TEXT,
            path TEXT
        );
        """
    )
    conn.commit()
    return conn


if __name__ == "__main__":
    connection = _temp_db_creation(
        r"C:\Users\zroy\Documents\_Python\calsim-scenario-server\example.sqlite"
    )
    dss = r"C:\Users\zroy\Documents\_Modeling\_2023DCR\_studies\9.0.0_danube_histadj\DSS\output\DCR2023_DV_9.0.0_Danube_Adj_v1.2.dss"

    if True:
        cur = connection.cursor()
        records = list()
        for i, (name, path) in enumerate(STANDARD_PATHS.items()):
            records.append((i, str(name), str(path)))

        cur.executemany(
            "INSERT INTO common_paths VALUES (?, ?, ?);",
            records,
        )
        connection.commit()

    if True:
        st = perf_counter()
        # Actual use case below
        cur = connection.cursor()
        with pdss.DSS(dss) as open_dss:
            add_to_data_ledger(
                cursor=cur,
                run_id=0,
                dss=open_dss,
                paths=STANDARD_PATHS,
            )
        connection.commit()
        et = perf_counter()
        print(et - st)

    if False:
        dss_out = r"C:\Users\zroy\Documents\_Python\calsim-scenario-server\example.dss"
        paths = tuple(p for p in STANDARD_PATHS.values())
        resolved_paths = list()
        with pdss.DSS(dss) as DSS_CHECK:
            for p in paths:
                p_resolved = DSS_CHECK.resolve_wildcard(p)
                if len(p_resolved) > 0:
                    resolved_paths.append(p_resolved.paths.pop())

        paths = tuple(zip(resolved_paths, resolved_paths))
        st = perf_counter()
        pdss.copy_multiple_rts(dss, dss_out, paths)
        et = perf_counter()
        print(et - st)
