from dataclasses import dataclass

from fastapi import Request
from jinja2 import Environment

from ...loader import ENV


@dataclass
class Error404:
    request: Request
    env: Environment = ENV
    template: str = "static/errors/error_404.jinja"

    def __str__(self) -> str:
        return self.env.get_template(self.template).render(request=self.request)

    def encode(self, charset: str) -> str:
        return str(self).encode(encoding=charset)
