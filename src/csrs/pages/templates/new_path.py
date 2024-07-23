from fastapi import Request
from jinja2 import Environment

from ..loader import ENV
from .form_parts import CreateStr, CreateStrLong


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
