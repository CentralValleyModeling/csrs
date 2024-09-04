import logging
from pathlib import Path

import pandss as pdss
from sqlalchemy.exc import IntegrityError

from .. import enums, schemas
from .base import Client


class RemoteClient(Client):
    """Client used to interact with a remote Results Server."""

    def __init__(self, base_url: str, **kwargs):
        """Initialize a client, and target a remote URL.

        Parameters
        ----------
        base_url : str
            The URL of the results server.
        kwargs
            All other keyword arguments are passed to httpx.Client()

        Example
        -------
        ```python-repl
        >>> import csrs
        >>> url = "calsim-scenario-results-server.azurewebsites.net"
        >>> client = csrs.RemoteClient(url)
        ```
        """
        self.actor = Client(base_url=base_url, **kwargs)
        self.logger = logging.getLogger(__name__)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(url={self.actor.base_url})"

    # GET
    def get_assumption_names(self) -> tuple[str]:
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
        url = "/assumptions"
        params = dict(kind=kind, name=name, id=id)
        params = {k: v for k, v in params.items() if v}
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return [schemas.Assumption.model_validate(a) for a in response.json()]

    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]:
        url = "/scenarios"
        params = dict(name=name, id=id)
        params = {k: v for k, v in params.items() if v}
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
    ) -> list[schemas.Run]:
        url = "/runs"
        params = dict(
            scenario=scenario,
            version=version,
            code_version=code_version,
            id=id,
        )
        params = {k: v for k, v in params.items() if v}
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
    ) -> list[schemas.NamedPath]:
        url = "/paths"
        params = dict(
            name=name,
            path=path,
            category=category,
            id=id,
        )
        params = {k: v for k, v in params.items() if v}
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return [schemas.NamedPath.model_validate(a) for a in response.json()]

    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries:
        url = "/timeseries"
        params = dict(
            scenario=scenario,
            version=version,
            path=path,
        )
        params = {k: v for k, v in params.items() if v}
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return schemas.Timeseries.model_validate(response.json())

    def get_timeseries_from_dss(
        self,
        dss: Path,
        scenario: str,
        version: str,
        paths: list[schemas.NamedPath] | None = None,
    ) -> list[schemas.Timeseries]:
        if paths is None:
            paths = self.get_path()
        tss = list()
        with pdss.DSS(dss) as dss_obj:
            for p in paths:
                try:
                    rtss = list(dss_obj.read_multiple_rts(p.path))
                except Exception as e:
                    self.logger.error(
                        f"{type(e)} when reading {p.path} in {dss}, skipping"
                    )
                    continue
                if len(rtss) == 0:
                    self.logger.warning(f"no datasets match {p.path} in {dss}")
                    continue
                elif len(rtss) > 1:
                    self.logger.warning(
                        f"multiple datasets match {p.path} in {dss}, "
                        + "skipping both to avoid conflicts"
                    )
                    continue
                rts = rtss[0]
                ts = schemas.Timeseries.from_pandss(
                    scenario=scenario,
                    version=version,
                    rts=rts,
                )
                ts.path = p.path  # Use the path from the database, not in the dss
                tss.append(ts)
        self.logger.info(
            f"{len(tss)} Timeseries found from {len(paths)} paths in {dss}"
        )
        return tss

    def get_all_timeseries_for_run(
        self,
        *,
        scenario: str,
        version: str,
    ) -> list[schemas.Timeseries]:
        url = "/timeseries/all"
        params = dict(
            scenario=scenario,
            version=version,
        )
        params = {k: v for k, v in params.items() if v}
        response = self.actor.get(url, params=params)
        response.raise_for_status()
        return [schemas.Timeseries.model_validate(ts) for ts in response.json()]

    # PUT

    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption:
        url = "/assumptions"
        obj = schemas.Assumption(name=name, kind=kind, detail=detail)
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Assumption.model_validate(response.json())

    def put_scenario(
        self,
        *,
        name: str,
        assumptions: dict[str, str],
    ) -> schemas.Scenario:
        url = "/scenarios"
        obj = schemas.Scenario(name=name, assumptions=assumptions)
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
        )
        url = "/runs"
        if not prefer_this_version:
            url = url + "/legacy"
        response = self.actor.put(url, json=obj.model_dump(mode="json"))
        response.raise_for_status()
        return schemas.Run.model_validate(response.json())

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
        obj = schemas.NamedPath(
            name=name,
            path=path,
            category=category,
            period_type=period_type,
            interval=interval,
            units=units,
            detail=detail,
        )
        url = "/paths"
        response = self.actor.put(url, json=obj.model_dump(mode="json", exclude=("id")))
        response.raise_for_status()
        return schemas.NamedPath.model_validate(response.json())

    def put_standard_paths(self) -> list[schemas.NamedPath]:
        url = "/paths"
        added = list()
        for p in enums.StandardPathsEnum:
            try:
                response = self.actor.put(
                    url,
                    json=p.value.model_dump(
                        mode="json",
                        exclude=("id"),
                    ),
                )
                response.raise_for_status()
                named = schemas.NamedPath.model_validate(response.json())
                added.append(named)
            except IntegrityError as e:
                self.logger.warning(
                    f"{type(e).__name__} occurred, likely due to one of the standard "
                    + "paths already exisitng on the database"
                )
            except Exception as e:
                path = p.value
                self.logger.error(
                    f"{type(e).__name__} occurred during path creation, skipping {path}"
                )
        return added

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

    def put_many_timeseries(
        self,
        timeseries: list[schemas.Timeseries],
    ) -> list[schemas.Timeseries]:
        url = "/timeseries"
        added = list()
        for ts in timeseries:
            try:
                response = self.actor.put(url, json=ts.model_dump(mode="json"))
                response.raise_for_status()
                ts_db = schemas.Timeseries.model_validate(response.json())
                added.append(ts_db)
            except Exception as e:
                self.logger.error(f"{type(e)} when adding {ts}, continuing")
        return added
