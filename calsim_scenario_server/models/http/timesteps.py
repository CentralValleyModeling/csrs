from pydantic import BaseModel


class TimeStepsModel(BaseModel):
    id: int
    datetime_str: str
