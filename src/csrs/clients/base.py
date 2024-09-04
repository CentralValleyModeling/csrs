import json
from pathlib import Path
from typing import NoReturn

import pandss as pdss

from .. import schemas


class Client:
    def __init__(self, *args, **kwargs):
        pass

    # GET
    def get_assumption_names(self) -> tuple[str]:
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
        raise NotImplementedError()

    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]:
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
        [Assumption(name=hist, kind=hydrology), Assumption(name=future, kind=hydrology)]
        ```
        """
        raise NotImplementedError()

    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]:
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
        raise NotImplementedError()

    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Run]:
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
        raise NotImplementedError()

    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedPath]:
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
        raise NotImplementedError()

    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries:
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

        raise NotImplementedError()

    def get_timeseries_from_dss(
        self,
        dss: Path,
        scenario: str,
        version: str,
        paths: list[schemas.NamedPath] | None = None,
    ) -> list[schemas.Timeseries]:
        raise NotImplementedError()

    def get_all_timeseries_for_run(
        self,
        *,
        scenario: str,
        version: str,
    ) -> list[schemas.Timeseries]:
        """Get all of the `Timeseries` objects for th run provided.

        Parameters
        ----------
        scenario : str
            Matches against `Run.scenario`. If provided this method will return at most
            one `Timeseries` object
        version : str
            Matches against `Run.version`. If provided this method will return at most
            one `Timeseries` object

        Returns
        -------
        list[schemas.Timeseries]
            The `Timeseries` object matched
        """
        raise NotImplementedError()

    # PUT

    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption:
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
        raise NotImplementedError()

    def put_scenario(
        self,
        *,
        name: str,
        assumptions: dict[str, str],
    ) -> schemas.Scenario:
        """Create a new `Scenario` on the results server.

        Parameters
        ----------
        name : str
            Value to assign to `Scenario.name`, should be easy to read, must be unique.
        assumptions: dict[str, str]
            Dictionary of assumption kinds to assumption names

        Returns
        -------
        schemas.Scenario
            The `Scenario` object created in the database.
        """
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
        raise NotImplementedError()

    def put_standard_paths(self) -> list[schemas.NamedPath]:
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
        raise NotImplementedError()

    def put_many_timeseries(
        self,
        timeseries: list[schemas.Timeseries],
    ) -> list[schemas.Timeseries]:
        raise NotImplementedError()

    # UTILITES
    def dump(self, dst: Path, **kwargs) -> NoReturn:
        database = {
            "assumptions": list(),
            "scenarios": list(),
            "paths": list(),
            "runs": list(),
            "timeseries": list(),
            "metrics": list(),
            "metric_values": list(),
        }

        for a in self.get_assumption():
            database["assumptions"].append(a.model_dump())
        for s in self.get_scenario():
            database["scenarios"].append(s.model_dump())
        for p in self.get_path():
            database["paths"].append(p.model_dump())
        for r in self.get_run():
            database["runs"].append(r.model_dump())
            for ts in self.get_all_timeseries_for_run(
                scenario=r.scenario, version=r.version
            ):
                database["timeseries"].append(ts.model_dump())
        # TODO: 2024-09-04 Add packing of metrics once those are implemented
        with open(dst, "w") as DST:
            json.dump(database, DST, **kwargs)
