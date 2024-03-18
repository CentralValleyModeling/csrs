import json
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Self

from packaging.version import Version


@dataclass(kw_only=True, frozen=True)
class Study:
    root: Path
    display_name: str
    author: str
    contact: str
    confidential: bool
    published: bool
    documentation: str
    scenario: dict

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.display_name})"

    @classmethod
    def from_json(cls, src: Path) -> Self:
        src = Path(src)
        if not src.exists():
            raise FileNotFoundError(src)
        # Read the class data from the given JSON
        with open(src, "r") as SRC:
            kwargs = json.load(SRC)
        if "root" not in kwargs:
            kwargs["root"] = src.parent
        kwargs["root"] = Path(kwargs["root"])
        # Do some validation
        missing = list()
        bad_types = list()
        for f in fields(cls):
            if f.name not in kwargs:
                missing.append(f.name)
            elif not isinstance(kwargs[f.name], f.type):
                bad_types.append((f.name, f.type, type(kwargs[f.name])))
        if missing:
            raise ValueError(
                "metadata for Study was not fully specified, "
                + "missing the following required fields:\n"
                + f"{missing}"
            )
        elif bad_types:
            raise TypeError(
                "metadata for Study was specified with improper types, "
                + "attribute, expected type, given type:\n"
                + "\n".join(",".join(tup) for tup in bad_types)
            )
        # If all clear, create the class
        return cls(**kwargs)

    def _get_history(self, top: Path, suffix: str) -> dict[Version, Path]:
        if suffix[0] != ".":
            suffix = f".{suffix}"
        if not top.exists():
            raise FileNotFoundError(top)
        files = [f for f in top.iterdir() if f.suffix == suffix]
        return {Version(f.stem.split("_v")[-1]): f for f in files}

    def _pick_from_files(
        self,
        files: dict[Version, Path],
        version: Version = None,
    ) -> Path:
        if version is None:
            version = sorted(list(files.keys()))[-1]
        elif not isinstance(version, Version):
            version = Version(version)  # Attempt to cast to Version object
        if version not in files:
            raise FileNotFoundError(
                "version requested not found:\n"
                + f"\trequested: {version}\n"
                + f"\tpresent:{tuple(files.keys())}"
            )

        return files[version]

    def get_sv(self, version: Version | str = None) -> Path:
        """Get the pathlib.Path to an SV file, defaults to the latest"""
        return self._pick_from_files(self.sv_files, version)

    def get_dv(self, version: Version | str = None) -> Path:
        """Get the pathlib.Path to a WSIDI file, defaults to the latest"""
        return self._pick_from_files(self.dv_files, version)

    @property
    def sv_dir(self) -> Path:
        """Get the pathlib.Path to the directory of SV files"""
        return self.root / "SV"

    @property
    def dv_dir(self) -> Path:
        """Get the pathlib.Path to the directory of WSIDI files"""
        return self.root / "DV"

    @property
    def sv_files(self) -> dict[Version, Path]:
        """A dict of pathlib.Path of SV files, keyed by the version numbers"""
        return self._get_history(self.sv_dir, ".dss")

    @property
    def dv_files(self) -> dict[Version, Path]:
        """A dict of pathlib.Path of WSIDI files, keyed by the version numbers"""
        return self._get_history(self.dv_dir, ".dss")

    @property
    def sv(self) -> Path:
        """A pathlib.Path of the latest SV file in the study"""
        return self.get_sv()

    @property
    def dv(self) -> Path:
        """A pathlib.Path of the latest WSIDI file in the study"""
        return self.get_dv()


@dataclass(kw_only=True)
class StudyDatabase:
    studies: list[Study]

    @classmethod
    def from_json(cls, src: Path) -> Self:
        src = Path(src)
        if not src.exists():
            raise FileNotFoundError(src)
        # Read the class data from the JSON
        with open(src, "r") as SRC:
            paths = json.load(SRC)
        # Do some validation
        if not isinstance(paths, list):
            raise ValueError(f"root of json expected to be list, found: {type(paths)}")
        studies = list()
        for p in paths:
            if not isinstance(p, str):
                raise ValueError(f"item in json expected to be str, found {type(p)}")
            metadata = src.parent / p / "metadata.json"
            studies.append(Study.from_json(metadata))
        return cls(studies=studies)

    def close(self):
        # Include for possible implemenation of database connections
        pass


def get_db():
    here = Path(__file__).parent
    db = StudyDatabase.from_json(here.parent / "database/names.json")
    try:
        yield db
    finally:
        db.close()
