from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Run, RunMetadata
from ..schemas import RunOut


def create(
    db: Session,
    name: str,
    scenario_id: int,
    version: str,
    contact: str,
    code_version: str,
    detail: str,
    published: bool = False,
    confidential: bool = True,
    predecessor_run_name: str = None,
) -> tuple[Run, RunMetadata]:
    if predecessor_run_name:
        predecessor_run = read(db, name=predecessor_run_name)
        if len(predecessor_run) != 1:
            raise HTTPException(
                status_code=400, detail="multiple potential predecessors found"
            )
        predecessor_run_id = predecessor_run[0].id
    else:
        predecessor_run_id = None

    # DB interactions
    run = Run(name=name, scenario_id=scenario_id, version=version)
    db.add(run)
    run_metadata = RunMetadata(
        run_id=run.id,
        predecessor_run_id=predecessor_run_id,
        contact=contact,
        confidential=confidential,
        published=published,
        code_version=code_version,
        detail=detail,
    )
    db.add(run_metadata)
    db.commit()
    db.refresh(run)
    db.refresh(run_metadata)
    return run, run_metadata


def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[RunOut]:
    filters = list()
    if name:
        filters.append(Run.name == name)
    if id:
        filters.append(Run.id == id)
    return (
        db.query(Run)
        .filter(*filters)
        .join(RunMetadata, Run.id == RunMetadata.run_id)
        .all()
    )


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
