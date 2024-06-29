from dataclasses import dataclass
from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, Template

from ... import schemas
from ..templates import templates
from ..utils import (
    EditableSelection,
    EditableSelectionGroup,
    EditableStr,
    EditableStrLong,
)


class EditableAssumption:
    def __init__(
        self,
        obj: schemas.Assumption,
        assumption_kinds: list[str],
    ):
        self.obj = obj
        self.kinds = assumption_kinds
        self.env: Environment = templates.env

    def render(self, request: Request) -> str:
        # Pre render the editable sections
        name = EditableStr(
            id=self.obj.id,
            name="name",
            default=self.obj.name,
        ).render(request)
        kind = EditableSelection(
            id=self.obj.id,
            name="kind",
            default=self.obj.kind,
            options=self.kinds,
        ).render(request)
        detail = EditableStrLong(
            id=self.obj.id,
            name="detail",
            default=self.obj.detail,
            rows=max(1, self.obj.detail.count("\n")),
        ).render(request)
        # render the whole card
        return self.env.get_template("objects/assumption.jinja").render(
            id=self.obj.id,
            title=self.obj.name,
            name=name,
            kind=kind,
            detail=detail,
            request=request,
        )


class EditableScenario:
    def __init__(
        self,
        obj: schemas.Scenario,
        scenario_versions: list[str],
        assumptions: list[schemas.Assumption],
    ):
        self.obj = obj
        self.versions = scenario_versions
        self.env: Environment = templates.env
        self.assumptions: dict[str, list[schemas.Assumption]] = dict()
        for a in assumptions:
            if a.kind not in self.assumptions:
                self.assumptions[a.kind] = list()
            self.assumptions[a.kind].append(a)

    def render(self, request: Request) -> str:
        # Pre render the editable sections
        name = EditableStr(
            id=self.obj.id,
            name="name",
            default=self.obj.name,
        ).render(
            request,
            name_col_width=2,
        )
        preferred_run = EditableSelection(
            id=self.obj.id,
            name="preferred_run",
            default=self.obj.preferred_run,
            options=self.versions,
        ).render(
            request,
            name_col_width=2,
        )
        assumptions_dropdowns = list()
        for kind, assumption_name in self.obj.assumptions.items():
            assumptions_dropdowns.append(
                EditableSelection(
                    id=self.obj.id,
                    name=kind,
                    default=assumption_name,
                    options=list(a.name for a in self.assumptions[kind]),
                )
            )
        assumptions = EditableSelectionGroup(
            name="assumptions",
            editable_selections=assumptions_dropdowns,
        ).render(request)

        # render the whole card
        return self.env.get_template("objects/scenario.jinja").render(
            request=request,
            id=self.obj.id,
            title=self.obj.name,
            name=name,
            preferred_run=preferred_run,
            assumptions=assumptions,
        )


class NewAssumption:
    def render(self):
        return Template("<p>New</p>").render()
