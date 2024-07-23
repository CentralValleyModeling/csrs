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


class NewAssumption:
    def __init__(
        self,
        assumption_kinds: list[str],
    ):
        self.kinds = assumption_kinds
        self.env: Environment = ENV

    def render(self, request: Request):
        name = CreateStr(
            id=0,
            name="name",
            description="The shorthand or colloquial name for this assumption",
        ).render(request)
        kind = CreateSelection(
            id=0,
            name="kind",
            default=self.kinds[0],
            options=self.kinds,
        ).render(request)
        detail = CreateStr(
            id=0,
            name="detail",
            description="A longer description of the assumption, used to explain"
            + " what the assumption entails",
            # rows=1,
        ).render(request)
        # render the whole card
        return self.env.get_template("templates/new_assumption.jinja").render(
            id=0,
            title="Create a New Assumption",
            name=name,
            kind=kind,
            detail=detail,
            request=request,
        )


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


class NewRuns:
    def __init__(
        self,
        scenarios: list[schemas.Scenario],
    ):
        self.scenarios = scenarios
        self.env: Environment = ENV

    def render(self, request: Request):
        scenario = CreateSelection(
            id=0,
            name="scenario",
            default=self.scenarios[0].name,
            options=[s.name for s in self.scenarios],
        ).render(request)
        version = CreateStr(
            id=0,
            name="version",
            description="The version of the Run, usually something like: `1.0.3`.",
        ).render(request)
        parent_version = CreateStr(
            id=0,
            name="parent",
            description="If this run is an update of a prior run, enter the version of"
            + " that run here. Otherwise, leave this blank.",
        ).render(request)
        contact = CreateStr(
            id=0,
            name="contact",
            description="An email, phone number, or similar. Can be used in the"
            + " future to answer questions about the data from the run.",
        ).render(request)
        confidential = CreateSwitch(
            id=0,
            name="confidential",
            default=True,
            env=self.env,
        ).render(request)
        published = CreateSwitch(
            id=0,
            name="published",
            default=False,
            env=self.env,
        ).render(request)
        code_version = CreateStr(
            id=0,
            name="code_version",
            description="The version code used to make the run, might be different"
            + " than the run version.",
        ).render(request)
        detail = CreateStrLong(
            id=0,
            name="detail",
            description="A longer description of the scenario, used to explain"
            + " what the scenario attempts to represent with it specific combination "
            + "of assumptions",
        ).render(request)

        # render the whole card
        return self.env.get_template("templates/new_run.jinja").render(
            id=0,
            title="Create a New Run",
            scenario=scenario,
            version=version,
            parent_version=parent_version,
            contact=contact,
            confidential=confidential,
            published=published,
            code_version=code_version,
            detail=detail,
            request=request,
        )


class NewPath:
    def __init__(self):
        self.env: Environment = ENV

    def render(self, request: Request):
        name = CreateStr(
            id=0,
            name="name",
            description="The shorthand name of the data the path contains.",
        ).render(request)
        path = CreateStr(
            id=0,
            name="path",
            description="/STUDY/TIMESERIES/GROUP/.*/INTERVAL/VERSION/",
        ).render(request)
        category = CreateStr(
            id=0,
            name="category",
            description="Information used to group paths of similar data types.",
        ).render(request)
        period_type = CreateStr(
            id=0,
            name="period_type",
            description="The HEC-DSS compliant period type, something like 'PER-AVER'.",
        ).render(request)
        interval = CreateStr(
            id=0,
            name="interval",
            description="The HEC-DSS compliant interval, something like '1MON'.",
        ).render(request)
        units = CreateStr(
            id=0,
            name="units",
            description="The units of the data in the timeseries.",
        ).render(request)
        detail = CreateStrLong(
            id=0,
            name="detail",
            description="A longer description of the path, used to explain"
            + " what the path represents",
        ).render(request)

        # render the whole card
        return self.env.get_template("templates/new_path.jinja").render(
            id=0,
            title="Create a New Path",
            name=name,
            path=path,
            category=category,
            period_type=period_type,
            interval=interval,
            units=units,
            detail=detail,
            request=request,
        )
