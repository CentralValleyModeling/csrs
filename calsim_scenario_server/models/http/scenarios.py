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


class ScenarioShortMetadata(BaseModel):
    name: str
