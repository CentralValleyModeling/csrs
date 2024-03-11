import json
from pathlib import Path


def from_json(src: Path = None) -> dict:
    if src is None:
        src = Path(__file__).parent / "app_metadata.json"
    with open(src, "r") as APP_METADATA:
        kwargs = json.load(APP_METADATA)
        return kwargs
