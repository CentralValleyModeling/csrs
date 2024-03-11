import xml.etree.cElementTree as ET
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


def rts_to_xml(rts: pdss.RegularTimeseries) -> ET.ElementTree:
    root = ET.Element("rts")

    path = ET.SubElement(root, "path")
    for k, v in rts.path.items():
        ET.SubElement(path, "part", name=k).text = v

    for f in fields(rts):
        if f in ("path", "dates", "values"):
            continue
        ET.SubElement(root, f.name).text = str(getattr(rts, f.name))

    values = ET.SubElement(root, "values")
    for v in rts.values.magnitude:
        ET.SubElement(values, "v").text = str(float(v))

    dates = ET.SubElement(root, "dates")
    for d in rts.dates:
        ET.SubElement(dates, "d").text = str(d)

    return root


def exceedance(rts: pdss.RegularTimeseries) -> dict[str, list[float]]:
    v = np.sort(rts.values.magnitude)
    e = 1.0 - np.arange(1.0, len(v) + 1.0) / len(v)
    return {"exceedance": list(e), "value": list(v)}


def cy_annual_exceedance(rts: pdss.RegularTimeseries) -> dict[str, list[float]]:
    df = rts.to_frame().resample(pd.offsets.YearEnd()).sum()
    v = np.sort(df.iloc[:, 0].values)
    e = 1.0 - np.arange(1.0, len(v) + 1.0) / len(v)
    return {"exceedance": list(e), "value": list(v)}


def wy_annual_exceedance(rts: pdss.RegularTimeseries) -> dict[str, list[float]]:
    df = rts.to_frame().resample(pd.offsets.MonthEnd()).sum()
    df.index = df.index + pd.Timedelta(days=92)
    df = df.resample(pd.offsets.YearEnd()).sum()
    v = np.sort(df.iloc[:, 0].values)
    e = 1.0 - np.arange(1.0, len(v) + 1.0) / len(v)
    return {"exceedance": list(e), "value": list(v)}
