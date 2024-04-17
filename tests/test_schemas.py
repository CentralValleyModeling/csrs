from calsim_scenario_server import schemas as s

EXPECTED_ASSUMPTION = {
    "id": int,
    "name": str,
    "kind": str,
    "detail": str,
}

EXPECTED_SCENARIO = {
    "id": int,
    "name": str,
    "version": str,
    "land_use": str,
    "sea_level_rise": str,
    "hydrology": str,
    "tucp": str,
    "dcp": str,
    "va": str,
    "south_of_delta": str,
}

EXPECTED_RUN = {
    "id": int,
    "scenario": str,
    "version": str,
    "parent_id": int,
    "children_ids": tuple,
    "contact": str,
    "confidential": bool,
    "published": bool,
    "code_version": str,
    "detail": bool,
}

EXPECTED_TIMESERIES = {
    "scenario": str,
    "version": str,
    "path": str,
    "values": tuple,
    "dates": tuple,
    "period_type": str,
    "units": str,
    "interval": str,
}

EXPECTED_PATH = {
    "id": int,
    "name": str,
    "path": str,
    "category": str,
    "detail": str,
}

EXPECTED_METRIC = {
    "id": int,
    "name": str,
    "index_detail": str,
    "detail": str,
}

EXPECTED_METRIC_VALUES = {
    "id": int,
    "scenario": str,
    "run_version": str,
    "path": str,
    "metric": str,
    "indexes": tuple,
    "values": tuple,
}

# TODO: add tests for schema structures
