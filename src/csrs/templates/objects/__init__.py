from dataclasses import dataclass
from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, Template

from ... import schemas
from ..templates import templates
from ..utils import EditableSelection, EditableStr, EditableStrLong


class EditableAssumption:
    def __init__(
        self,
        assumption_object: schemas.Assumption,
        assumption_kinds: list[str],
    ):
        self.obj = assumption_object
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


@dataclass
class NewAssumption:
    def render(self):
        return Template("<p>New</p>").render()
