from sqlalchemy.orm import Session

from ..models import RunModel
from ..schemas import Run
from . import scenarios as crud_scenarios
from .decorators import rollback_on_exception


@rollback_on_exception
def model_to_schema(run: RunModel) -> Run:
    if run.parent:
        parent = run.parent.version
    else:
        parent = None
    if run.children:
        children = tuple(c.version for c in run.children)
    else:
        children = tuple()
    return Run(
        scenario=run.scenario.name,
        version=run.version,
        # info
        parent=parent,
        children_ids=children,
        contact=run.contact,
        confidential=run.confidential,
        published=run.published,
        code_version=run.code_version,
        detail=run.detail,
    )


@rollback_on_exception
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
    dss: str = None,
    prefer_this_version: bool = True,
) -> Run:
    if predecessor_run_name:
        predecessor_run = read(db, name=predecessor_run_name)
        if len(predecessor_run) != 1:
            raise AttributeError("multiple potential predecessors found")
        predecessor_run_id = predecessor_run[0].id
    else:
        predecessor_run_id = None
    (scenario_model,) = crud_scenarios.read(db=db, name=scenario)

    run = RunModel(
        scenario_id=scenario_model.id,
        version=version,
        parent_id=predecessor_run_id,
        contact=contact,
        code_version=code_version,
        detail=detail,
        published=published,
        confidential=confidential,
        dss=dss,
    )
    db.add(run)
    if prefer_this_version:
        crud_scenarios.update_version(db, scenario, version)
    db.commit()
    db.refresh(run)

    return model_to_schema(run)


def read(
    db: Session,
    scenario: str = None,
    version: str = None,
    code_version: str = None,
    contact: str = None,
    id: int = None,
) -> list[Run]:
    filters = list()
    if scenario:
        (scenario_obj,) = crud_scenarios.read(db, name=scenario)
        filters.append(RunModel.scenario_id == scenario_obj.id)
    if version:
        filters.append(RunModel.version == version)
    if code_version:
        filters.append(RunModel.code_version == code_version)
    if id:
        filters.append(RunModel.id == id)
    if contact:
        filters.append(RunModel.contact == contact)
    runs = db.query(RunModel).filter(*filters).all()
    return [model_to_schema(r) for r in runs]


def update():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
