from dataclasses import dataclass

from fastapi import Request
from jinja2 import Environment

from .loader import ENV


@dataclass
class Home:
    request: Request
    env: Environment = ENV
    template: str = "home.jinja"

    def __str__(self) -> str:
        return self.env.get_template(self.template).render(request=self.request)

    def encode(self, charset: str) -> str:
        return str(self).encode(encoding=charset)
