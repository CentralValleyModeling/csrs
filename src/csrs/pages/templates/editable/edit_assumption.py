from fastapi import Request
from jinja2 import Environment

from .... import schemas
from ...loader import ENV
from ..forms import EditableSelection, EditableStr, EditableStrLong


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
        return self.env.get_template("templates/editable/edit_assumption.jinja").render(
            edit_on=edit_on,
            id=self.obj.id,
            title=self.obj.name,
            name=name,
            kind=kind,
            detail=detail,
            request=request,
        )
