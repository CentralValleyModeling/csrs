from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import Environment

templates = Jinja2Templates(directory=str(Path(__file__).parent))
env: Environment = templates.env
