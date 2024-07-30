import os

from fastapi import Request
from sqlalchemy.orm import Session

from .. import crud, errors
from . import loader, templates

ALLOW_EDITING_VIA_FORMS = bool(os.getenv("ALLOW_EDITING_VIA_FORMS", True))


def render_assumptions(request: Request, db: Session):
    all_objs = crud.assumptions.read(db=db)
    all_kinds = crud.assumptions.read_kinds(db=db)
    objects = [templates.EditableAssumption(obj, all_kinds) for obj in all_objs]
    metadata = loader.ENV.get_template("static/metadata/assumption.jinja").render()
    return loader.jinja_loader.TemplateResponse(
        "templates/edit.jinja",
        {
            "request": request,
            "page_title": "Assumptions",
            "metadata": metadata,
            "objects": objects,
            "new_object": templates.NewAssumption(all_kinds),
            "edit_on": ALLOW_EDITING_VIA_FORMS,
        },
    )


def render_scenarios(request: Request, db: Session):
    all_objs = crud.scenarios.read(db=db)
    all_assumptions = crud.assumptions.read(db=db)
    objects = list()
    for obj in all_objs:
        try:
            versions = [r.version for r in crud.runs.read(db=db, scenario=obj.name)]
        except errors.EmptyLookupError:
            versions = ["No Runs for Scenario"]
        t = templates.EditableScenario(obj, versions, all_assumptions)
        objects.append(t)
    metadata = loader.ENV.get_template("static/metadata/scenario.jinja").render()
    return loader.jinja_loader.TemplateResponse(
        "templates/edit.jinja",
        {
            "request": request,
            "page_title": "Scenarios",
            "metadata": metadata,
            "objects": objects,
            "new_object": templates.NewScenario(all_assumptions),
            "edit_on": ALLOW_EDITING_VIA_FORMS,
        },
    )


def render_runs(request: Request, db: Session):
    all_objs = crud.runs.read(db=db)
    all_scenarios = crud.scenarios.read(db=db)
    objects = list()
    for obj in all_objs:
        t = templates.EditableRuns(obj)
        objects.append(t)
    metadata = loader.ENV.get_template("static/metadata/run.jinja").render()
    return loader.jinja_loader.TemplateResponse(
        "templates/edit.jinja",
        {
            "request": request,
            "page_title": "Runs",
            "metadata": metadata,
            "objects": objects,
            "new_object": templates.NewRuns(all_scenarios),
            "edit_on": ALLOW_EDITING_VIA_FORMS,
        },
    )


def render_paths(request: Request, db: Session):
    all_objs = crud.paths.read(db=db)
    objects = list()
    for obj in all_objs:
        t = templates.EditablePaths(obj)
        objects.append(t)
    metadata = loader.ENV.get_template("static/metadata/path.jinja").render()
    return loader.jinja_loader.TemplateResponse(
        "templates/edit.jinja",
        {
            "request": request,
            "page_title": "Named Paths",
            "metadata": metadata,
            "objects": objects,
            "new_object": templates.NewPath(),
            "edit_on": ALLOW_EDITING_VIA_FORMS,
        },
    )
