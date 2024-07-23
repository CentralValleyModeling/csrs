from fastapi import Request
from jinja2 import Environment

from ... import schemas
from ..loader import ENV
from .form_parts import EditableSelection, EditableSelectionGroup, EditableStr


class EditableScenario:
    def __init__(
        self,
        obj: schemas.Scenario,
        scenario_versions: list[str],
        assumptions: list[schemas.Assumption],
    ):
        self.obj = obj
        self.versions = scenario_versions
        self.env: Environment = ENV
        self.assumptions: dict[str, list[schemas.Assumption]] = dict()
        for a in assumptions:
            if a.kind not in self.assumptions:
                self.assumptions[a.kind] = list()
            self.assumptions[a.kind].append(a)

    def render(self, request: Request, edit_on: bool = True) -> str:
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
            try:
                options = list(a.name for a in self.assumptions[kind])
            except KeyError:
                options = list()
            assumptions_dropdowns.append(
                EditableSelection(
                    id=self.obj.id,
                    name=kind,
                    default=assumption_name,
                    options=options,
                )
            )
        assumptions = EditableSelectionGroup(
            name="assumptions",
            editable_selections=assumptions_dropdowns,
        ).render(request)

        # render the whole card
        return self.env.get_template("templates/edit_scenario.jinja").render(
            edit_on=edit_on,
            request=request,
            id=self.obj.id,
            title=self.obj.name,
            name=name,
            preferred_run=preferred_run,
            assumptions=assumptions,
        )
