from dataclasses import dataclass, field

from fastapi import Request
from jinja2 import Environment

from ..templates import templates


@dataclass
class EditableStr:
    id: int | str
    name: str
    default: str
    env: Environment = field(default=templates.env)

    def render(self, request: Request, **kwargs) -> str:
        return self.env.get_template("utils/editable_str.jinja").render(
            request=request,
            id=self.id,
            name=self.name,
            default=self.default,
            **kwargs,
        )


@dataclass
class EditableStrLong:
    id: int | str
    name: str
    default: str
    rows: int = 1
    env: Environment = field(default=templates.env)

    def render(self, request: Request, **kwargs) -> str:
        return self.env.get_template("utils/editable_str_long.jinja").render(
            request=request,
            id=self.id,
            name=self.name,
            default=self.default,
            rows=self.rows,
            **kwargs,
        )


@dataclass
class EditableSelection:
    id: int | str
    name: str
    default: str
    options: list[str]
    env: Environment = field(default=templates.env)

    def render(self, request: Request, **kwargs) -> str:
        return self.env.get_template("utils/editable_selection.jinja").render(
            request=request,
            id=self.id,
            name=self.name,
            default=self.default,
            options=self.options,
            **kwargs,
        )
