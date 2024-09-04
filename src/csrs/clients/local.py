import logging
from pathlib import Path

import pandss as pdss
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from .. import crud, enums, errors, models, schemas
from .base import Client


class LocalClient(Client):
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
        self.logger = logging.getLogger(__name__)
        models.Base.metadata.create_all(bind=self.engine)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(db_path={self.db_path})"

    def close(self):
        self.session.close()
        self.engine.dispose()

    # annotations and type hints are in pyi file
    # GET
    def get_assumption_names(self) -> tuple[str]:
        return crud.assumptions.read_kinds(db=self.session)

    def get_assumption(
        self,
        *,
        kind: str = None,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Assumption]:
        return crud.assumptions.read(db=self.session, kind=kind, name=name, id=id)

    def get_scenario(
        self,
        *,
        name: str = None,
        id: int = None,
    ) -> list[schemas.Scenario]:
        return crud.scenarios.read(db=self.session, name=name, id=id)

    def get_run(
        self,
        *,
        scenario: str = None,
        version: str = None,
        code_version: str = None,
        id: int = None,
    ) -> list[schemas.Run]:
        return crud.runs.read(
            db=self.session,
            scenario=scenario,
            version=version,
            code_version=code_version,
            id=id,
        )

    def get_path(
        self,
        *,
        name: str = None,
        path: str = None,
        category: str = None,
        id: str = None,
    ) -> list[schemas.NamedPath]:
        return crud.paths.read(
            db=self.session,
            name=name,
            path=path,
            category=category,
            id=id,
        )

    def get_timeseries(
        self,
        *,
        scenario: str,
        version: str,
        path: str,
    ) -> schemas.Timeseries:
        return crud.timeseries.read(
            db=self.session,
            scenario=scenario,
            version=version,
            path=path,
        )

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
        try:
            return crud.timeseries.read_all_for_run(
                self.session,
                scenario=scenario,
                version=version,
            )
        except errors.EmptyLookupError:
            return []

    # PUT
    def put_assumption(
        self,
        *,
        name: str,
        kind: str,
        detail: str,
    ) -> schemas.Assumption:
        obj = schemas.Assumption(
            name=name,
            kind=kind,
            detail=detail,
        )
        return crud.assumptions.create(
            db=self.session, **obj.model_dump(exclude=("id"))
        )

    def put_scenario(
        self,
        *,
        name: str,
        assumptions: dict[str, str],
    ) -> schemas.Scenario:
        obj = schemas.Scenario(name=name, assumptions=assumptions)
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
        )
        return crud.runs.create(
            db=self.session,
            prefer_this_version=prefer_this_version,
            **obj.model_dump(exclude=("id")),
        )

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
        return crud.paths.create(db=self.session, **obj.model_dump(exclude=("id")))

    def put_standard_paths(self) -> list[schemas.NamedPath]:
        added = list()
        for p in enums.StandardPathsEnum:
            try:
                named = crud.paths.create(
                    db=self.session, **p.value.model_dump(exclude=("id"))
                )
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
        return crud.timeseries.create(db=self.session, **obj.model_dump())

    def put_many_timeseries(
        self,
        timeseries: list[schemas.Timeseries],
    ) -> list[schemas.Timeseries]:
        added = list()
        for ts in timeseries:
            try:
                ts_db = crud.timeseries.create(
                    db=self.session,
                    **ts.model_dump(exclude="id"),
                )
                added.append(ts_db)
            except Exception as e:
                self.logger.error(f"{type(e)} when adding {ts}, continuing")

        return added
