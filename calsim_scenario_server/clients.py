from pathlib import Path
from typing import Iterable, overload

import pandss as pdss
from httpx import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from . import crud, enums, models, schemas
from .logger import logger


class ClientABC:
    def get_assumption_names(self) -> list[str]:
        raise NotImplementedError()

    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]:
        raise NotImplementedError()

    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]:
        raise NotImplementedError()

    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Run]:
        raise NotImplementedError()

    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedDatasetPath]:
        raise NotImplementedError()

    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries:
        raise NotImplementedError()

    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption:
        raise NotImplementedError()

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
    ) -> schemas.Scenario:
        raise NotImplementedError()

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
    ) -> schemas.Run:
        raise NotImplementedError()

    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        detail: str,
    ) -> schemas.NamedDatasetPath:
        raise NotImplementedError()

    def put_default_paths(self) -> None:
        raise NotImplementedError()

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
    ) -> schemas.Timeseries:
        raise NotImplementedError()

    def put_many_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        dss: Path,
        paths: Iterable[schemas.NamedDatasetPath] = None,
    ) -> list[schemas.Timeseries]:
        raise NotImplementedError()


class RemoteClient(ClientABC):
    def __init__(self, base_url: str):
        self.actor = Client(base_url=base_url)

    # annotations and type hints are in pyi file
    # GET
    def get_assumption_names(self) -> list[str]:
        url = "/assumptions/names"
        response = self.actor.get(url)
        response.raise_for_status()
        return response.json()

    @overload
    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]: ...

    def get_assumption(self, **kwargs):
        url = "/assumptions"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.Assumption.model_validate(a) for a in response.json()]

    @overload
    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...

    def get_scenario(self, **kwargs):
        url = "/scenarios"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.Scenario.model_validate(a) for a in response.json()]

    @overload
    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...

    def get_run(self, **kwargs):
        url = "/runs"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.Run.model_validate(a) for a in response.json()]

    @overload
    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedDatasetPath]: ...

    def get_path(self, **kwargs):
        url = "/paths"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.NamedDatasetPath.model_validate(a) for a in response.json()]

    @overload
    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries: ...

    def get_timeseries(self, **kwargs):
        url = "/timeseries"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return schemas.Timeseries.model_validate(response.json())

    # PUT
    @overload
    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption: ...

    def put_assumption(self, **kwargs):
        obj = schemas.Assumption(**kwargs)
        url = "/assumptions"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Assumption.model_validate(response.json())

    @overload
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

    def put_scenario(self, **kwargs):
        obj = schemas.Scenario(**kwargs)
        url = "/scenarios"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Scenario.model_validate(response.json())

    @overload
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

    def put_run(self, **kwargs):
        obj = schemas.Run(**kwargs)
        url = "/runs"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Run.model_validate(response.json())

    @overload
    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        detail: str,
    ) -> schemas.NamedDatasetPath: ...

    def put_path(self, **kwargs):
        obj = schemas.NamedDatasetPath(**kwargs)
        url = "/paths"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.NamedDatasetPath.model_validate(response.json())

    def put_default_paths(self) -> None:
        logger.debug(f"adding paths from {enums.StandardPathsEnum}")
        for p in enums.StandardPathsEnum:
            self.put_path(**p.value.model_dump(exclude=("id")))

    @overload
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

    def put_timeseries(self, **kwargs):
        obj = schemas.Timeseries(**kwargs)
        url = "/timeseries"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Timeseries.model_validate(response.json())

    def put_many_timeseries(
        self,
        scenario: str,
        version: str,
        dss: Path,
        paths: Iterable[schemas.NamedDatasetPath] = None,
    ) -> list[schemas.Timeseries]:
        url = "/timeseries"
        if paths is None:
            paths = [p.value for p in enums.StandardPathsEnum]
        added = list()
        with pdss.DSS(dss) as dss_obj:
            for p in paths:
                rts = dss_obj.read_rts(p.path)
                ts = schemas.Timeseries.from_pandss(scenario, version, rts)
                response = self.actor.put(url, json=ts.model_dump(mode="json"))
                response.raise_for_status()
                added.append(schemas.Timeseries.model_validate(response.json()))
        return added


class LocalClient(ClientABC):
    def __init__(
        self,
        db_path: Path,
        echo: bool = False,
        autocommit: bool = False,
        autoflush: bool = True,
        check_same_thread: bool = True,
    ):
        self.db_path = Path(db_path).resolve()
        self.engine = create_engine(
            "sqlite:///" + str(self.db_path),
            connect_args={
                "check_same_thread": check_same_thread,
            },
            poolclass=SingletonThreadPool,
            echo=echo,
        )
        self.session = sessionmaker(
            autocommit=autocommit,
            autoflush=autoflush,
            bind=self.engine,
        )()
        models.Base.metadata.create_all(bind=self.engine)

    def close(self):
        self.session.close()
        self.engine.dispose()

    # annotations and type hints are in pyi file
    # GET
    def get_assumption_names(self):
        logger.debug("get_assumption_names")
        return schemas.Scenario.get_assumption_attrs()

    @overload
    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]: ...

    def get_assumption(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.assumptions.read(db=self.session, **kwargs)

    @overload
    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...

    def get_scenario(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.scenarios.read(db=self.session, **kwargs)

    @overload
    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...

    def get_run(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.runs.read(db=self.session, **kwargs)

    @overload
    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedDatasetPath]: ...

    def get_path(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.paths.read(db=self.session, **kwargs)

    @overload
    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries: ...

    def get_timeseries(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.timeseries.read(db=self.session, **kwargs)

    # PUT
    @overload
    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption: ...

    def put_assumption(self, **kwargs):
        obj = schemas.Assumption(**kwargs)
        logger.debug(f"{obj=}")
        return crud.assumptions.create(
            db=self.session, **obj.model_dump(exclude=("id"))
        )

    @overload
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

    def put_scenario(self, **kwargs):
        obj = schemas.Scenario(**kwargs)
        logger.debug(f"{obj=}")
        return crud.scenarios.create(db=self.session, **obj.model_dump(exclude=("id")))

    @overload
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

    def put_run(self, **kwargs):
        obj = schemas.Run(**kwargs)
        logger.debug(f"{obj=}")
        return crud.runs.create(db=self.session, **obj.model_dump(exclude=("id")))

    @overload
    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        detail: str,
    ) -> schemas.NamedDatasetPath: ...

    def put_path(self, **kwargs):
        obj = schemas.NamedDatasetPath(**kwargs)
        logger.debug(f"{obj=}")
        return crud.paths.create(db=self.session, **obj.model_dump(exclude=("id")))

    def put_default_paths(self):
        logger.debug(f"adding paths from {enums.StandardPathsEnum}")
        for p in enums.StandardPathsEnum:
            self.put_path(**p.value.model_dump(exclude=("id")))

    @overload
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

    def put_timeseries(self, **kwargs):
        obj = schemas.Timeseries(**kwargs)
        logger.debug(f"{obj=}")
        return crud.timeseries.create(db=self.session, **obj.model_dump())

    def put_many_timeseries(
        self,
        scenario: str,
        version: str,
        dss: Path,
        paths: Iterable[schemas.NamedDatasetPath] = None,
    ):
        if paths is None:
            paths = [p.value for p in enums.StandardPathsEnum]
        with pdss.DSS(dss) as dss_obj:
            for p in paths:
                rts = dss_obj.read_rts(p.path)
                ts = schemas.Timeseries.from_pandss(scenario, version, rts)
                crud.timeseries.create(db=self.session, **ts.model_dump())
