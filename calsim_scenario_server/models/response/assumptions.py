from pydantic import BaseModel


class AssumptionDetails(BaseModel):
    detail: str


class AssumptionSummary(BaseModel):
    name: str
    rows: int
    column_names: list[str]
