# flake8: noqa
import pandss as pdss

from . import schemas

class ScenarioManager:
    def get_assumption_names(self) -> list[str]: ...
    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]: ...
    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...
    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Run]: ...
    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedDatasetPath]: ...
    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries: ...
    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption: ...
    def put_scenario(
        self,
        *,
        name: str,
        land_use: str,
        sea_level_rise: str,
        hydrology: str,
        tucp: str,
        dcp: str,
        va: str,
        south_of_delta: str,
        version: str = None,
    ) -> schemas.Scenario: ...
    def put_run(
        self,
        *,
        scenario: str,
        version: str,
        contact: str,
        code_version: str,
        detail: str,
        # optional
        parent: str | None = None,
        children: tuple[str, ...] = tuple(),
        confidential: bool = True,
        published: bool = False,
        prefer_this_version: bool = True,
    ) -> schemas.Run: ...
    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        detail: str,
    ) -> schemas.NamedDatasetPath: ...
    def put_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        # shadow pandss RegularTimeseries attributes
        path: str | pdss.DatasetPath,
        values: tuple[float, ...],
        dates: tuple[str, ...],
        period_type: str,
        units: str,
        interval: str,
    ) -> schemas.Timeseries: ...

class RemoteClient(ScenarioManager):
    def get_assumption_names(self) -> list[str]: ...
    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]: ...
    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...
    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...
    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedDatasetPath]: ...
    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries: ...
    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> list[schemas.Assumption]: ...
    def put_scenario(
        self,
        *,
        name: str,
        land_use: str,
        sea_level_rise: str,
        hydrology: str,
        tucp: str,
        dcp: str,
        va: str,
        south_of_delta: str,
        version: str = None,
    ) -> schemas.Scenario: ...
    def put_run(
        self,
        *,
        scenario: str,
        version: str,
        contact: str,
        code_version: str,
        detail: str,
        # optional
        parent: str | None = None,
        children: tuple[str, ...] = tuple(),
        confidential: bool = True,
        published: bool = False,
        prefer_this_version: bool = True,
    ) -> schemas.Run: ...
    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        detail: str,
    ) -> schemas.NamedDatasetPath: ...
    def put_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        # shadow pandss RegularTimeseries attributes
        path: str | pdss.DatasetPath,
        values: tuple[float, ...],
        dates: tuple[str, ...],
        period_type: str,
        units: str,
        interval: str,
    ) -> schemas.Timeseries: ...

class LocalClient(ScenarioManager):
    def close() -> None: ...
    def get_assumption_names(self) -> list[str]: ...
    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]: ...
    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...
    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Run]: ...
    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedDatasetPath]: ...
    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries: ...
    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption: ...
    def put_scenario(
        self,
        *,
        name: str,
        land_use: str,
        sea_level_rise: str,
        hydrology: str,
        tucp: str,
        dcp: str,
        va: str,
        south_of_delta: str,
        version: str = None,
    ) -> schemas.Scenario: ...
    def put_run(
        self,
        *,
        scenario: str,
        version: str,
        contact: str,
        code_version: str,
        detail: str,
        # optional
        parent: str | None = None,
        children: tuple[str, ...] = tuple(),
        confidential: bool = True,
        published: bool = False,
        prefer_this_version: bool = True,
    ) -> schemas.Run: ...
    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        detail: str,
    ) -> schemas.NamedDatasetPath: ...
    def put_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        # shadow pandss RegularTimeseries attributes
        path: str | pdss.DatasetPath,
        values: tuple[float, ...],
        dates: tuple[str, ...],
        period_type: str,
        units: str,
        interval: str,
    ) -> schemas.Timeseries: ...
