from fastapi import Request
from jinja2 import Environment

from .... import schemas
from ...loader import ENV
from ..forms import CreateSelection, CreateStr, CreateStrLong, CreateSwitch


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
        return self.env.get_template("templates/new/new_run.jinja").render(
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
