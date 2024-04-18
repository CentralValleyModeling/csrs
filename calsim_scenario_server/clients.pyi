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
    ) -> list[schemas.Scenario]: ...
    def get_timeseries(
        self,
        *,
        scenario: str = None,
        version: str = None,
        path: str = None,
    ) -> list[schemas.Timeseries]: ...
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
    ) -> list[schemas.Scenario]: ...
    def put_run(
        self,
        *,
        scenario: str,
        version: str,
        parent: str | None = None,
        children: tuple[str, ...] = tuple(),
        contact: str,
        confidential: bool = True,
        published: bool = False,
        code_version: str,
        detail: str,
    ) -> list[schemas.Scenario]: ...
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
    ) -> list[schemas.Timeseries]: ...

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
    def get_timeseries(
        self,
        *,
        scenario: str = None,
        version: str = None,
        path: str = None,
    ) -> list[schemas.Timeseries]: ...
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
    ) -> list[schemas.Scenario]: ...
    def put_run(
        self,
        *,
        scenario: str,
        version: str,
        parent: str | None = None,
        children: tuple[str, ...] = tuple(),
        contact: str,
        confidential: bool = True,
        published: bool = False,
        code_version: str,
        detail: str,
    ) -> list[schemas.Scenario]: ...
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
    ) -> list[schemas.Timeseries]: ...

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
    ) -> list[schemas.Scenario]: ...
    def get_timeseries(
        self,
        *,
        scenario: str = None,
        version: str = None,
        path: str = None,
    ) -> list[schemas.Timeseries]: ...
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
    ) -> list[schemas.Scenario]: ...
    def put_run(
        self,
        *,
        scenario: str,
        version: str,
        parent: str | None = None,
        children: tuple[str, ...] = tuple(),
        contact: str,
        confidential: bool = True,
        published: bool = False,
        code_version: str,
        detail: str,
    ) -> list[schemas.Scenario]: ...
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
    ) -> list[schemas.Timeseries]: ...