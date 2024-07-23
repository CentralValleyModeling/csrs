from dataclasses import dataclass
from pathlib import Path

from fastapi import Request
from jinja2 import Environment, Template

from ... import schemas
from ..loader import ENV
from .editable import EditableAssumption, EditablePaths, EditableRuns, EditableScenario
from .form_parts import (
    CreateSelection,
    CreateSelectionGroup,
    CreateStr,
    CreateStrLong,
    CreateSwitch,
)
from .new import NewAssumption, NewPath, NewRuns, NewScenario
