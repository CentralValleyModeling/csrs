from pydantic import BaseModel


class PathModel(BaseModel):
    id: int = None
    path: str
    category: str
    detail: str
