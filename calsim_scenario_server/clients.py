from pathlib import Path
from typing import Iterable

import pandss as pdss
from httpx import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from . import crud, enum, models, schemas
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

    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]:
        params = dict(kind=kind, name=name, id=id)
        params = {k: v for k, v in params.items() if v}
        url = "/assumptions"
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return [schemas.Assumption.model_validate(a) for a in response.json()]

    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]:
        params = dict(name=name, id=id)
        params = {k: v for k, v in params.items() if v}
        url = "/scenarios"
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return [schemas.Scenario.model_validate(a) for a in response.json()]

    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]:
        params = dict(
            scenario=scenario,
            version=version,
            code_version=code_version,
            id=id,
        )
        params = {k: v for k, v in params.items() if v}
        url = "/runs"
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return [schemas.Run.model_validate(a) for a in response.json()]

    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedDatasetPath]:
        params = dict(name=name, path=path, category=category, id=id)
        params = {k: v for k, v in params.items() if v}
        url = "/paths"
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return [schemas.NamedDatasetPath.model_validate(a) for a in response.json()]

    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries:
        params = dict(scenario=scenario, version=version, path=path)
        params = {k: v for k, v in params.items() if v}
        url = "/timeseries"
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return schemas.Timeseries.model_validate(response.json())

    # PUT
    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption:
        obj = schemas.Assumption(name=name, kind=kind, detail=detail)
        url = "/assumptions"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Assumption.model_validate(response.json())

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
        obj = schemas.Scenario(
            name=name,
            land_use=land_use,
            sea_level_rise=sea_level_rise,
            hydrology=hydrology,
            tucp=tucp,
            dcp=dcp,
            va=va,
            south_of_delta=south_of_delta,
            version=version,
        )
        url = "/scenarios"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Scenario.model_validate(response.json())

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
        obj = schemas.Run(
            scenario=scenario,
            version=version,
            contact=contact,
            code_version=code_version,
            detail=detail,
            parent=parent,
            children=children,
            confidential=confidential,
            published=published,
            prefer_this_version=prefer_this_version,
        )
        url = "/runs"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Run.model_validate(response.json())

    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        detail: str,
    ) -> schemas.NamedDatasetPath:
        obj = schemas.NamedDatasetPath(
            name=name,
            path=path,
            category=category,
            detail=detail,
        )
        url = "/paths"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.NamedDatasetPath.model_validate(response.json())

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
        obj = schemas.Timeseries(
            scenario=scenario,
            version=version,
            path=path,
            values=values,
            dates=dates,
            period_type=period_type,
            units=units,
            interval=interval,
        )
        url = "/timeseries"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Timeseries.model_validate(response.json())


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

    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]:
        params = dict(kind=kind, name=name, id=id)
        params = {k: v for k, v in params.items() if v}
        logger.debug(f"{params=}")
        return crud.assumptions.read(db=self.session, **params)

    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]:
        params = dict(name=name, id=id)
        params = {k: v for k, v in params.items() if v}
        logger.debug(f"{params=}")
        return crud.scenarios.read(db=self.session, **params)

    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]:
        params = dict(
            scenario=scenario,
            version=version,
            code_version=code_version,
            id=id,
        )
        params = {k: v for k, v in params.items() if v}
        logger.debug(f"{params=}")
        return crud.runs.read(db=self.session, **params)

    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedDatasetPath]:
        params = dict(name=name, path=path, category=category, id=id)
        params = {k: v for k, v in params.items() if v}
        logger.debug(f"{params=}")
        return crud.paths.read(db=self.session, **params)

    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries:
        params = dict(scenario=scenario, version=version, path=path)
        params = {k: v for k, v in params.items() if v}
        logger.debug(f"{params=}")
        return crud.timeseries.read(db=self.session, **params)

    # PUT
    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption:
        obj = schemas.Assumption(name=name, kind=kind, detail=detail)
        logger.debug(f"{obj=}")
        return crud.assumptions.create(
            db=self.session, **obj.model_dump(exclude=("id"))
        )

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
        obj = schemas.Scenario(
            name=name,
            land_use=land_use,
            sea_level_rise=sea_level_rise,
            hydrology=hydrology,
            tucp=tucp,
            dcp=dcp,
            va=va,
            south_of_delta=south_of_delta,
            version=version,
        )
        logger.debug(f"{obj=}")
        return crud.scenarios.create(db=self.session, **obj.model_dump(exclude=("id")))

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
        obj = schemas.Run(
            scenario=scenario,
            version=version,
            contact=contact,
            code_version=code_version,
            detail=detail,
            parent=parent,
            children=children,
            confidential=confidential,
            published=published,
            prefer_this_version=prefer_this_version,
        )
        logger.debug(f"{obj=}")
        return crud.runs.create(db=self.session, **obj.model_dump(exclude=("id")))

    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        detail: str,
    ) -> schemas.NamedDatasetPath:
        obj = schemas.NamedDatasetPath(
            name=name,
            path=path,
            category=category,
            detail=detail,
        )
        logger.debug(f"{obj=}")
        return crud.paths.create(db=self.session, **obj.model_dump(exclude=("id")))

    def put_default_paths(self):
        logger.debug(f"adding paths from {enum.StandardPathsEnum}")
        paths = [p.value for p in enum.StandardPathsEnum]
        for p in paths:
            self.put_path(**p.model_dump(exclude=("id")))

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
        obj = schemas.Timeseries(
            scenario=scenario,
            version=version,
            path=path,
            values=values,
            dates=dates,
            period_type=period_type,
            units=units,
            interval=interval,
        )
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
            paths = [p.value for p in enum.StandardPathsEnum]

        with pdss.DSS(dss) as dss_obj:
            for p in paths:
                rts = dss_obj.read_rts(p.path)
                ts = schemas.Timeseries.from_pandss(scenario, version, rts)
                crud.timeseries.create(db=self.session, **ts.model_dump())

    # TODO: 2024-04-18 Add ability to upload timeseries from DSS
    # TODO: 2024-04-18 Add ability to upload run and all timeseries from one method
