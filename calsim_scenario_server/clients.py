from pathlib import Path

import pandss as pdss
from httpx import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from . import crud, models, schemas
from .logger import logger


class ScenarioManager:
    pass


class RemoteClient(ScenarioManager):
    def __init__(self, base_url: str):
        self.actor = Client(base_url=base_url)

    # annotations and type hints are in pyi file
    # GET
    def get_assumption_names(self):
        url = "/assumptions/names"
        response = self.actor.get(url)
        response.raise_for_status()
        return response.json()

    def get_assumption(self, **kwargs):
        url = "/assumptions"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.Assumption.model_validate(a) for a in response.json()]

    def get_scenario(self, **kwargs):
        url = "/scenarios"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.Scenario.model_validate(a) for a in response.json()]

    def get_run(self, **kwargs):
        url = "/runs"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.Run.model_validate(a) for a in response.json()]

    def get_path(self, **kwargs):
        url = "/paths"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.NamedDatasetPath.model_validate(a) for a in response.json()]

    def get_timeseries(self, **kwargs):
        url = "/timeseries"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return schemas.Timeseries.model_validate(response.json())

    # PUT
    def put_assumption(self, **kwargs):
        obj = schemas.Assumption(**kwargs)
        url = "/assumptions"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Assumption.model_validate(response.json())

    def put_scenario(self, **kwargs):
        obj = schemas.Scenario(**kwargs)
        url = "/scenarios"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Scenario.model_validate(response.json())

    def put_run(self, **kwargs):
        obj = schemas.Run(**kwargs)
        url = "/runs"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Run.model_validate(response.json())

    def put_path(self, **kwargs):
        obj = schemas.NamedDatasetPath(**kwargs)
        url = "/paths"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.NamedDatasetPath.model_validate(response.json())

    def put_timeseries(self, **kwargs):
        obj = schemas.Timeseries(**kwargs)
        url = "/timeseries"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Timeseries.model_validate(response.json())


class LocalClient(ScenarioManager):
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

    def get_assumption(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.assumptions.read(db=self.session, **kwargs)

    def get_scenario(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.scenarios.read(db=self.session, **kwargs)

    def get_run(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.runs.read(db=self.session, **kwargs)

    def get_path(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.paths.read(db=self.session, **kwargs)

    def get_timeseries(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.timeseries.read(db=self.session, **kwargs)

    # PUT
    def put_assumption(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.assumptions.create(db=self.session, **kwargs)

    def put_scenario(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.scenarios.create(db=self.session, **kwargs)

    def put_run(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.runs.create(db=self.session, **kwargs)

    def put_path(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.paths.create(db=self.session, **kwargs)

    def put_timeseries(self, **kwargs):
        logger.debug(f"{kwargs=}")
        return crud.timeseries.create(db=self.session, **kwargs)

    # TODO: 2024-04-18 Add ability to upload timeseries from DSS
    # TODO: 2024-04-18 Add ability to upload run and all timeseries from one method
