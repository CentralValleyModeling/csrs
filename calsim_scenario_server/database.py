import tomllib
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Self


@dataclass(kw_only=True)
class Study:
    name: str
    sv: str
    dv: str

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        for f in fields(cls):
            if f.name not in d:
                d[f.name] = None
        return cls(**d)


class StudyDatabase:
    def __init__(self, config: Path):
        self.config = config

    def read_config(self) -> dict:
        with open(self.config, "rb") as config:
            return tomllib.load(config)

    def get_studies(self) -> list[Study]:
        config = self.read_config()
        return [Study.from_dict(d) for d in config["studies"]]

    @property
    def studies(self) -> list[Study]:
        return self.get_studies()

    def close(self):
        pass
