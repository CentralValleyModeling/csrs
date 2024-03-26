from pydantic import BaseModel


class PathModel(BaseModel):
    path: str
    category: str
    detail: str
