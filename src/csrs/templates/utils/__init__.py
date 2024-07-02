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
        return self.env.get_template("utils/editable_attr_str.jinja").render(
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
        return self.env.get_template("utils/editable_attr_str_long.jinja").render(
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
        return self.env.get_template("utils/editable_attr_selection.jinja").render(
            request=request,
            id=self.id,
            name=self.name,
            default=self.default,
            options=self.options,
            **kwargs,
        )


@dataclass
class EditableSelectionGroup:
    name: str
    editable_selections: list[EditableSelection]
    env: Environment = field(default=templates.env)

    def render(self, request: Request, **kwargs) -> str:
        sections = list()
        for edit_sel in self.editable_selections:
            sections.append(
                edit_sel.render(
                    request,
                    name_col_width=2,
                )
            )
        return self.env.get_template(
            "utils/editable_attr_selection_group.jinja"
        ).render(
            request=request,
            name=self.name,
            sections=sections,
        )


@dataclass
class EditableSwitch:
    id: int
    name: str
    default: bool
    env: Environment = field(default=templates.env)

    def render(self, request: Request, **kwargs) -> str:
        status = ""
        if self.default:
            status = "checked"
        return self.env.get_template("utils/editable_attr_switch.jinja").render(
            id=self.id,
            request=request,
            name=self.name,
            default=status,
        )


@dataclass
class CreateStr:
    id: int | str
    name: str
    description: str
    env: Environment = field(default=templates.env)

    def render(self, request: Request, **kwargs) -> str:
        return self.env.get_template("utils/create_attr_str.jinja").render(
            request=request,
            id=self.id,
            name=self.name,
            description=self.description,
            **kwargs,
        )
