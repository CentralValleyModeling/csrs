from pydantic import BaseModel

from .scenarios import ScenarioShortMetadata


class RunShortMetadata(BaseModel):
    name: str
    version: str
    detail: str


class RunFullMetadata(BaseModel):
    name: str
    version: str
    predecessor_run: RunShortMetadata
    contact: str
    confidential: bool
    published: bool
    code_version: str
    detail: str
    scenario: ScenarioShortMetadata


class RunSubmission(BaseModel):
    name: str
    scenario_id: int
    version: str
    contact: str
    confidential: bool
    published: bool
    code_version: str
    detail: str
    predecessor_run_id: int | None
