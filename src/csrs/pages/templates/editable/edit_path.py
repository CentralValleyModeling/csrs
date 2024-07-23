from fastapi import Request
from jinja2 import Environment

from .... import schemas
from ...loader import ENV
from ..form_parts import EditableStr, EditableStrLong


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
        return self.env.get_template("templates/editable/edit_path.jinja").render(
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
