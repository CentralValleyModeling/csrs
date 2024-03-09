from dataclasses import fields

import numpy as np
import pandas as pd
import pandss as pdss


def rts_to_json(rts: pdss.RegularTimeseries) -> dict:
    d = {f.name: getattr(rts, f.name) for f in fields(rts)}
    d["values"] = tuple(float(v) for v in rts.values.magnitude)
    d["dates"] = pd.to_datetime(rts.dates).strftime("%Y-%m-%dT%H:%M:%SZ").to_list()
    d["interval"] = str(rts.interval)

    return d


def exceedance(rts: pdss.RegularTimeseries) -> list[tuple[float, float]]:
    v = np.sort(rts.values.magnitude)
    e = 1.0 - np.arange(1.0, len(v) + 1.0) / len(v)
    return [(e[i], v[i]) for i in range(len(v))]


def cy_annual_exceedance(rts: pdss.RegularTimeseries) -> list[tuple[float, float]]:
    df = rts.to_frame().resample(pd.offsets.YearEnd()).sum()
    v = np.sort(df.iloc[:, 0].values)
    e = 1.0 - np.arange(1.0, len(v) + 1.0) / len(v)
    return [(e[i], v[i]) for i in range(len(v))]


def wy_annual_exceedance(rts: pdss.RegularTimeseries) -> list[tuple[float, float]]:
    df = rts.to_frame().resample(pd.offsets.MonthEnd()).sum()
    df.index = df.index + pd.Timedelta(days=92)
    df = df.resample(pd.offsets.YearEnd()).sum()
    v = np.sort(df.iloc[:, 0].values)
    e = 1.0 - np.arange(1.0, len(v) + 1.0) / len(v)
    return [(e[i], v[i]) for i in range(len(v))]
