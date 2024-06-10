from pathlib import Path
from typing import Iterable, overload
from warnings import warn

import pandss as pdss
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from csrs import crud, enums, models, schemas


class LocalClient:
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
    def get_assumption_names(self) -> tuple[enums.AssumptionEnum]:
        return crud.assumptions.read_kinds(db=self.session)

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
        assumpionts: dict[str, str],
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
