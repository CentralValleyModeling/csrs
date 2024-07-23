from fastapi import Request
from jinja2 import Environment

from ...loader import ENV
from ..form_parts import CreateSelection, CreateStr


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
        return self.env.get_template("templates/new/new_assumption.jinja").render(
            id=0,
            title="Create a New Assumption",
            name=name,
            kind=kind,
            detail=detail,
            request=request,
        )
