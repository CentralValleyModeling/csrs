from pydantic import BaseModel

from .assumptions import AssumptionDetails


class ScenarioFullMetadata(BaseModel):
    name: str
    land_use: AssumptionDetails
    sea_level_rise: AssumptionDetails
    hydrology: AssumptionDetails
    tucp: AssumptionDetails
    dcp: AssumptionDetails
    va: AssumptionDetails
    sod: AssumptionDetails


class ScenarioIdMetadata(BaseModel):
    name: str
    land_use_id: int
    sea_level_rise_id: int
    hydrology_id: int
    tucp_id: int
    dcp_id: int
    va_id: int
    sod_id: int


class ScenarioShortMetadata(BaseModel):
    name: str