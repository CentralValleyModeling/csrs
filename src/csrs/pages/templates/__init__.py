from dataclasses import dataclass
from pathlib import Path

from fastapi import Request
from jinja2 import Environment, Template

from ... import schemas
from ..loader import ENV
from .edit_assumption import EditableAssumption
from .edit_path import EditablePaths
from .edit_run import EditableRuns
from .edit_scenario import EditableScenario
from .form_parts import (
    CreateSelection,
    CreateSelectionGroup,
    CreateStr,
    CreateStrLong,
    CreateSwitch,
)
from .new_assumption import NewAssumption
from .new_path import NewPath
from .new_run import NewRuns
from .new_scenario import NewScenario
