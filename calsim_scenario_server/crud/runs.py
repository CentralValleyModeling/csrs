from sqlalchemy.orm import Session

from ..models import RunMetadataModel, RunModel
from ..schemas import Run
from .scenarios import read as read_scenarios


def model_to_schema(run: RunModel) -> Run:
    if run.parent:
        parent_id = run.parent.id
    else:
        parent_id = None
    if run.children:
        children = [c.id for c in run.children]
    else:
        children = None
    return Run(
        scenario_id=run.scenario_id,
        version=run.version,
        # info
        parent_id=parent_id,
        children_ids=children,
        contact=run.info.contact,
        confidential=run.info.confidential,
        published=run.info.published,
        code_version=run.info.code_version,
        detail=run.info.detail,
    )


def create(
    db: Session,
    scenario: str,
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
            raise AttributeError("multiple potential predecessors found")
        predecessor_run_id = predecessor_run[0].id
    else:
        predecessor_run_id = None
    (scenario_model,) = read_scenarios(db=db, name=scenario)

    # DB interactions
    run = RunModel(
        scenario_id=scenario_model.id,
        version=version,
        parent_id=predecessor_run_id,
    )
    db.add(run)
    db.flush()
    run_metadata = RunMetadataModel(
        run_id=run.id,
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

    return model_to_schema(run)


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
