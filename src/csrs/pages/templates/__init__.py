from dataclasses import dataclass
from pathlib import Path

from fastapi import Request
from jinja2 import Environment, Template

from ... import schemas
from ..loader import ENV
from .form_parts import (
    CreateSelection,
    CreateSelectionGroup,
    CreateStr,
    CreateStrLong,
    CreateSwitch,
    EditableSelection,
    EditableSelectionGroup,
    EditableStr,
    EditableStrLong,
    EditableSwitch,
)


class EditableAssumption:
    def __init__(
        self,
        obj: schemas.Assumption,
        assumption_kinds: list[str],
    ):
        self.obj = obj
        self.kinds = assumption_kinds
        self.env: Environment = ENV

    def render(self, request: Request, edit_on: bool = True) -> str:
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
        return self.env.get_template("templates/assumption.jinja").render(
            edit_on=edit_on,
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
        return self.env.get_template("templates/scenario.jinja").render(
            edit_on=edit_on,
            request=request,
            id=self.obj.id,
            title=self.obj.name,
            name=name,
            preferred_run=preferred_run,
            assumptions=assumptions,
        )


class EditableRuns:
    def __init__(
        self,
        obj: schemas.Run,
    ):
        self.obj = obj
        self.env: Environment = ENV

    def render(self, request: Request, edit_on: bool = True) -> str:
        _id = self.obj.id
        scenario = EditableStr(
            id=_id,
            name="scenario",
            default=self.obj.scenario,
        ).render(
            request,
            toggle_tag="",
        )
        version = EditableStr(
            id=_id,
            name="version",
            default=self.obj.version,
        ).render(
            request,
            toggle_tag="",
        )
        contact = EditableStr(
            id=_id,
            name="contact",
            default=self.obj.contact,
        ).render(request)
        confidential = EditableSwitch(
            id=_id,
            name="confidential",
            default=self.obj.confidential,
        ).render(request)
        published = EditableSwitch(
            id=_id,
            name="published",
            default=self.obj.published,
        ).render(request)
        code_version = EditableStr(
            id=_id,
            name="code_version",
            default=self.obj.code_version,
        ).render(request)
        detail = EditableStrLong(
            id=_id,
            name="detail",
            default=self.obj.detail,
        ).render(request)
        return self.env.get_template("templates/run.jinja").render(
            edit_on=edit_on,
            request=request,
            title=f"{self.obj.scenario} <code>(v{self.obj.version})</code>",
            scenario=scenario,
            version=version,
            contact=contact,
            confidential=confidential,
            published=published,
            code_version=code_version,
            detail=detail,
            id=self.obj.id,
        )


class EditablePaths:
    def __init__(
        self,
        obj: schemas.NamedPath,
    ):
        self.obj = obj
        self.env: Environment = ENV

    def render(self, request: Request, edit_on: bool = True) -> str:
        _id = self.obj.id
        name = EditableStr(
            id=_id,
            name="name",
            default=self.obj.name,
        ).render(request)
        path = EditableStr(
            id=_id,
            name="path",
            default=self.obj.path,
        ).render(request)
        category = EditableStr(
            id=_id,
            name="category",
            default=self.obj.category,
        ).render(request)
        detail = EditableStrLong(
            id=_id,
            name="detail",
            default=self.obj.detail,
        ).render(request)
        period_type = EditableStr(
            id=_id,
            name="period_type",
            default=self.obj.period_type,
        ).render(request)
        interval = EditableStr(
            id=_id,
            name="interval",
            default=self.obj.interval,
        ).render(request)
        units = EditableStr(
            id=_id,
            name="units",
            default=self.obj.units,
        ).render(request)
        return self.env.get_template("templates/path.jinja").render(
            edit_on=edit_on,
            request=request,
            title=self.obj.name,
            name=name,
            path=path,
            category=category,
            detail=detail,
            period_type=period_type,
            interval=interval,
            units=units,
            id=self.obj.id,
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
