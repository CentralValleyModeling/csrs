from pathlib import Path
from typing import Iterable, overload
from warnings import warn

import pandss as pdss
from httpx import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from . import crud, enums, models, schemas


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
    ) -> list[schemas.NamedPath]:
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
        period_type: str,
        interval: str,
        units: str,
        detail: str,
    ) -> schemas.NamedPath:
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
        paths: Iterable[schemas.NamedPath] = None,
    ) -> list[schemas.Timeseries]:
        raise NotImplementedError()


class RemoteClient(ClientABC):
    """Client used to interact with a remote Results Server."""

    def __init__(self, base_url: str):
        """Initialize a client, and target a remote URL.

        Parameters
        ----------
        base_url : str
            The URL of the results server.

        Example
        -------
        ```python-repl
        >>> import csrs
        >>> url = "calsim-scenario-results-server.azurewebsites.net"
        >>> client = csrs.RemoteClient(url)
        ```
        """
        self.actor = Client(base_url=base_url)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(url={self.actor.base_url})"

    # GET
    def get_assumption_names(self) -> list[str]:
        """Get the list of assumption categories that each scenario requires.

        Returns
        -------
        list[str]
            A list of names of assumption categories

        Example
        -------
        ```python-repl
        >>> client.get_assumption_names()
        ["land_use", "hydrology", "sea_level_rise"]
        ```

        """
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
        """Get the `Assumption` objects that match the information provided.

        If no arguments are given, all Assumption objects in the database will be
        returned.

        Parameters
        ----------
        kind : str, optional
            Matches against `Assumption.kind`, use `get_assumption_names` to get the
            full list of assumption types, by default None
        name : str, optional
            Matches against `Assumption.name`. If provided, this method will return at
            most one `Assumption` object, by default None
        id : int, optional
            Matches against `Assumption.id`. If provided, this method will return at
            most one `Assumption` object, by default None

        Returns
        -------
        list[schemas.Assumption]
            All of the `Assumption` objects that were matched.

        Example
        -------
        ```python-repl
        >>> client.get_assumption(kind="hydrolgy")
        [Assumption(name="Historical"), Assumption(name="Future")]
        ```
        """
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
        """Get the `Scenario` objects that match the information provided.

        Parameters
        ----------
        name : str, optional
            Matches against `Scenario.name`. If provided, this method will return at
            most one `Scenario` object, by default None
        id : int, optional
            Matches against `Scenario.id`. If provided, this method will return at most
            one `Scenario` object, by default None

        Returns
        -------
        list[schemas.Scenario]
            All of the `Scenario` objects that were matched.
        """

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
    ) -> list[schemas.Run]: ...

    def get_run(self, **kwargs):
        """Get the `Run` objects that match the information provided.

        Parameters
        ----------
        scenario : str, optional
            Matches against `Run.scenario`, by default None
        version : str, optional
            Matches against `Run.version`. If provided, this method will return at most
            one `Run` object, by default None
        code_version : str, optional
            Matches against `Run.code_version`, by default None
        id : int, optional
            Matches against `Run.id`. If provided, this method will return at most one
            `Run` object, by default None

        Returns
        -------
        list[schemas.Run]
            All of the `Run` objects that were matched.
        """

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
    ) -> list[schemas.NamedPath]: ...

    def get_path(self, **kwargs):
        """Get the `NamedPath` objects that match the information provided.

        Parameters
        ----------
        name : str, optional
            Matches against `NamedPath.name`. If provided, this method will return at
            most one `NamedPath` object, by default None
        path : str, optional
            Matches against `NamedPath.path`. If provided, this method will return at
            most one `NamedPath` object, by default None
        category : str, optional
            Matches against `NamedPath.category`, by default None
        id : str, optional
            Matches against `NamedPath.id`. If provided this method will return at most
            one `NamedPath` object, by default None

        Returns
        -------
        list[schemas.NamedPath]
            All of the `NamedPath` objects that were matched.
        """

        url = "/paths"
        response = self.actor.get(url, params=kwargs)
        response.raise_for_status()
        return [schemas.NamedPath.model_validate(a) for a in response.json()]

    @overload
    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries: ...

    def get_timeseries(self, **kwargs):
        """Get the `Timeseries` object that matches the information provided.

        Parameters
        ----------
        scenario : str
            Matches against `Run.scenario`. If provided this method will return at most
            one `Timeseries` object
        version : str
            Matches against `Run.version`. If provided this method will return at most
            one `Timeseries` object
        path : str
            Matches against `Timeseries.path`. If provided this method will return at
            most one `Timeseries` object

        Returns
        -------
        schemas.Timeseries
            The `Timeseries` object matched
        """

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
        """Create a new `Assumption` on the results server.

        Parameters
        ----------
        name : str
            The name of the `Assumption`
        kind : str
            The type of `Assumption`, should be a member of `csrs.enums.AssumptionEnum`
        detail : str
            A description and metadata for the assumption.

        Returns
        -------
        schemas.Assumption
            The `Assumption` object created
        """

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
        """Create a new `Scenario` on the results server.

        Parameters
        ----------
        name : str
            Value to assign to `Scenario.name`, should be easy to read, must be unique.
        land_use : str
            The name of the `Assumption` to tag as the `land_use` assumption.
        sea_level_rise : str
            The name of the `Assumption` to tag as the `sea_level_rise` assumption.
        hydrology : str
            The name of the `Assumption` to tag as the `hydrology` assumption.
        tucp : str
            The name of the `Assumption` to tag as the `tucp` assumption.
        dcp : str
            The name of the `Assumption` to tag as the `dcp` assumption.
        va : str
            The name of the `Assumption` to tag as the `va` assumption.
        south_of_delta : str
            The name of the `Assumption` to tag as the `south_of_delta` assumption.
        version : str, optional
            The preferred version of the `Run` for this `Scenario`, by default None

        Returns
        -------
        schemas.Scenario
            The `Scenario` object created in the database.
        """
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
        """Create a new `Run` on the results server.

        Parameters
        ----------
        scenario : str
            The name of the `Scenario` this `Run` should be assigned to.
        version : str
            The `version` of this run in the `Scenario` context, suggested to follow the
            `major.minor` pattern.
        contact : str
            Contact information for the modeler knowledgable about the run results.
        code_version : str
            The version of the code base, will likely differ from the `Run.version`.
        detail : str
            A description of the run, and it's purpose. This is where metadata regarding
            the `Run`, it's results, and it's changes compared to it's parents should be
            written.
        parent : str | None, optional
            The `Run` that this version was based on, by default None
        children : tuple[str, ...], optional
            The `Run` objects that are immediately based on this `Run`, usually not
            specified on __init__, by default tuple()
        confidential : bool, optional
            Whether or not this `Run` data is confidential, by default True
        published : bool, optional
            Whether or not this `Run` data has been published, by default False
        prefer_this_version : bool, optional
            Each `Scenario` prefers a single `Run`, if this is `True` the `Scenario` ]
            will be updated to prefer this new `Run`, by default True

        Returns
        -------
        schemas.Run
            The newly created `Run` object
        """

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
        period_type: str,
        interval: str,
        units: str,
        detail: str,
    ) -> schemas.NamedPath: ...

    def put_path(self, **kwargs):
        """Create a new `NamedPath` on the results server.

        Parameters
        ----------
        name : str
            The name of the path, should be easy to read, and unique
        path : str
            The A-F DSS path corresponding to the NamedPath data
        category : str
            A category to help organize similar paths
        period_type : str
            The `period_type` of the DSS timeseries
        interval : str
            The `interval` of the DSS timeseries
        units : str
            The `units` of the DSS timeseries
        detail : str
            A description of, and metadata for the data represented by the path

        Returns
        -------
        schemas.NamedPath
            The `NamedPath` object created
        """

        obj = schemas.NamedPath(**kwargs)
        url = "/paths"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.NamedPath.model_validate(response.json())

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
        """Create a new `Timeseries` on the results server

        Parameters
        ----------
        scenario : str
            The name of the `Scenario` that this data should be assigned to
        version : str
            The verson of the `Run` that this data should be assigned to
        path : str | pdss.DatasetPath
            The path of the `NamedPath` that this data should be assigned to
        values : tuple[float, ...]
            The values for the timeseries
        dates : tuple[str, ...]
            The ISO formatted dates for the timeseries
        period_type : str
            The `period_type` of the DSS data for the timeseries
        units : str
            The `units` of the DSS data for the timeseries
        interval : str
            The `interval` of the DSS data for the timeseries

        Returns
        -------
        schemas.Timeseries
            The `Timeseries` object that was created
        """

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
        paths: Iterable[schemas.NamedPath] = None,
    ) -> list[schemas.Timeseries]:
        """Create multiple `Timeseries` objects from a DSS file.

        The datasets to be extracted are specified as an iterable of `NamedPath`
        objects, but it will default to uploading the data for all the paths in
        `csrs.enums.StandardPathsEnum`.

        Parameters
        ----------
        scenario : str
            The name of the `Scenario` that this data should be assigned to
        version : str
            The verson of the `Run` that this data should be assigned to
        dss : Path
            The DSS file to extract data from
        paths : Iterable[schemas.NamedPath], optional
            The collection of Paths to extract from the DSS file, by default
            `csrs.enums.StandardPathsEnum`

        Returns
        -------
        list[schemas.Timeseries]
            The `Timeseries` object created

        Raises
        ------
        ValueError
            Raised of the collection of paths is incorrectly given
        """
        url = "/timeseries"
        if paths is None:
            paths = [p.value for p in enums.StandardPathsEnum]
        elif not isinstance(paths[0], schemas.NamedPath):
            raise ValueError(f"paths not given as {schemas.NamedPath}")
        added = list()
        with pdss.DSS(dss) as dss_obj:
            for p in paths:
                try:
                    rts = dss_obj.read_rts(p.path)
                except pdss.errors.UnexpectedDSSReturn:
                    warn(f"couldn't read {p} from {dss}")
                    continue
                # Add path
                p.path = str(rts.path)
                found_paths = self.get_path(
                    name=p.name,
                    path=p.path,
                    category=p.category,
                )
                if not found_paths:
                    self.actor.put("/paths", json=p.model_dump(exclude=("id")))
                # Add timeseries
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
        return crud.assumptions.read(db=self.session, **kwargs)

    @overload
    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]: ...

    def get_scenario(self, **kwargs):
        return crud.scenarios.read(db=self.session, **kwargs)

    @overload
    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Run]: ...

    def get_run(self, **kwargs):
        return crud.runs.read(db=self.session, **kwargs)

    @overload
    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedPath]: ...

    def get_path(self, **kwargs):
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
        return crud.runs.create(db=self.session, **obj.model_dump(exclude=("id")))

    @overload
    def put_path(
        self,
        *,
        name: str,
        path: str,
        category: str,
        period_type: str,
        interval: str,
        units: str,
        detail: str,
    ) -> schemas.NamedPath: ...

    def put_path(self, **kwargs):
        obj = schemas.NamedPath(**kwargs)
        return crud.paths.create(db=self.session, **obj.model_dump(exclude=("id")))

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
        return crud.timeseries.create(db=self.session, **obj.model_dump())

    def put_many_timeseries(
        self,
        scenario: str,
        version: str,
        dss: Path,
        paths: Iterable[schemas.NamedPath] = None,
    ) -> list[schemas.Timeseries]:
        if paths is None:
            paths = [p.value for p in enums.StandardPathsEnum]
        elif not isinstance(paths[0], schemas.NamedPath):
            raise ValueError(f"paths not given as {schemas.NamedPath}")
        added = list()
        with pdss.DSS(dss) as dss_obj:
            for p in paths:
                try:
                    rts = dss_obj.read_rts(p.path)
                except pdss.errors.UnexpectedDSSReturn:
                    warn(f"couldn't read {p} from {dss}, (UnexpectedDSSReturn)")
                    continue
                except ValueError:
                    warn(f"couldn't read {p} from {dss}, (ValueError)")
                    continue
                # Add path
                p.path = str(rts.path)
                found_paths = crud.paths.read(
                    db=self.session,
                    name=p.name,
                    path=p.path,
                    category=p.category,
                )
                if not found_paths:
                    crud.paths.create(db=self.session, **p.model_dump(exclude=("id")))
                # Add timeseries
                ts = schemas.Timeseries.from_pandss(scenario, version, rts)
                kwargs = ts.model_dump()
                kwargs["path"] = str(rts.path)
                ts = crud.timeseries.create(db=self.session, **kwargs)
                added.append(ts)
        return added
