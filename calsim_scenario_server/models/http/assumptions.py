from pydantic import BaseModel, Field


class AssumptionDetails(BaseModel):
    detail: str
    additional_fields: dict = Field(default_factory=dict)


class AssumptionSummary(BaseModel):
    name: str
    rows: int
    column_names: list[str]
