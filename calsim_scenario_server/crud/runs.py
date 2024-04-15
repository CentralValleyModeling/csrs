from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import RunMetadataModel, RunModel
from ..schemas import Run


def model_to_schema(run: RunModel, meta: RunMetadataModel, db: Session) -> Run:
    if meta.predecessor_run_id is not None:
        pred = (
            db.query(RunModel)
            .filter(RunModel.id == RunMetadataModel.predecessor_run_id)
            .first()
            .name
        )
    else:
        pred = None
    return Run(
        name=run.name,
        scenario_id=run.scenario_id,
        predecessor_run_name=pred,
        contact=meta.contact,
        confidential=meta.confidential,
        published=meta.published,
        code_version=meta.code_version,
        detail=meta.detail,
    )


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
) -> Run:
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
    run = RunModel(name=name, scenario_id=scenario_id, version=version)
    db.add(run)
    run_metadata = RunMetadataModel(
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

    return model_to_schema(run, run_metadata, db)


def read(
    db: Session,
    name: str = None,
    id: int = None,
) -> list[Run]:
    filters = list()
    if name:
        filters.append(RunModel.name == name)
    if id:
        filters.append(RunModel.id == id)
    runs = (
        db.query(RunModel)
        .filter(*filters)
        .join(RunMetadataModel, RunModel.id == RunMetadataModel.run_id)
        .all()
    )
    # TODO: parse the joined table to a list of objects, need to find predecessor by id


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
