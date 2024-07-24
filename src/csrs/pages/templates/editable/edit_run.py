from fastapi import Request
from jinja2 import Environment

from .... import schemas
from ...loader import ENV
from ..forms import EditableStr, EditableStrLong, EditableSwitch


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
        return self.env.get_template("templates/editable/edit_run.jinja").render(
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
