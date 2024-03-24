from pydantic import BaseModel


class AssumptionDetails(BaseModel):
    detail: str
