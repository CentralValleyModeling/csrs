from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import Environment

jinja_loader = Jinja2Templates(directory=str(Path(__file__).parent))
ENV: Environment = jinja_loader.env
