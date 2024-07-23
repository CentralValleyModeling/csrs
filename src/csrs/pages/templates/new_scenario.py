from fastapi import Request
from jinja2 import Environment

from ... import schemas
from ..loader import ENV
from .form_parts import CreateSelection, CreateSelectionGroup, CreateStr


class NewScenario:
    def __init__(
        self,
        assumptions: list[schemas.Assumption],
    ):
        self.assumptions = assumptions
        self.env: Environment = ENV

    def render(self, request: Request):
        name = CreateStr(
            id=0,
            name="name",
            description="The shorthand or colloquial name for this assumption",
        ).render(request)
        assumptions: dict[str, list] = dict()
        for a in self.assumptions:
            if a.kind not in assumptions:
                assumptions[a.kind] = list()
            assumptions[a.kind].append(a.name)
        assumptions = {k: sorted(v) for k, v in assumptions.items()}
        sections = list()
        for kind, options in assumptions.items():
            sections.append(
                CreateSelection(
                    id="new",
                    name=kind,
                    default=options[0],
                    options=options,
                    env=self.env,
                )
            )
        assumptions = CreateSelectionGroup(
            name="assumptions",
            new_selections=sections,
            env=self.env,
        ).render(request)

        # render the whole card
        return self.env.get_template("templates/new_scenario.jinja").render(
            id=0,
            title="Create a New Scenario",
            name=name,
            assumptions=assumptions,
            request=request,
        )
