from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import crud, errors, templates
from ..database import get_db
from ..logger import logger

ALLOW_EDITING_VIA_FORMS = True
router = APIRouter(prefix="/forms", include_in_schema=False)


###############################################################################
# RENDER
# Below are page rendering functions


def render_assumptions(request: Request, db: Session):
    all_objs = crud.assumptions.read(db=db)
    all_kinds = crud.assumptions.read_kinds(db=db)
    objects = [templates.EditableAssumption(obj, all_kinds) for obj in all_objs]
    return templates.templates.TemplateResponse(
        "pages/edit.jinja",
        {
            "request": request,
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
        versions = [r.version for r in crud.runs.read(db=db, scenario=obj.name)]
        t = templates.EditableScenario(obj, versions, all_assumptions)
        objects.append(t)
    return templates.templates.TemplateResponse(
        "pages/edit.jinja",
        {
            "request": request,
            "objects": objects,
            "new_object": templates.NewScenario(),
            "edit_on": ALLOW_EDITING_VIA_FORMS,
        },
    )


def render_runs(request: Request, db: Session):
    all_objs = crud.runs.read(db=db)
    objects = list()
    for obj in all_objs:
        t = templates.EditableRuns(obj)
        objects.append(t)
    return templates.templates.TemplateResponse(
        "pages/edit.jinja",
        {
            "request": request,
            "objects": objects,
            "new_object": templates.NewRuns(),
            "edit_on": ALLOW_EDITING_VIA_FORMS,
        },
    )


def render_timeseries(request: Request, db: Session):
    all_objs = crud.paths.read(db=db)
    objects = list()
    for obj in all_objs:
        t = templates.EditablePaths(obj)
        objects.append(t)
    return templates.templates.TemplateResponse(
        "pages/edit.jinja",
        {
            "request": request,
            "objects": objects,
            "new_object": templates.NewPath(),
            "edit_on": ALLOW_EDITING_VIA_FORMS,
        },
    )


def render_paths(request: Request, db: Session):
    all_objs = crud.paths.read(db=db)
    objects = list()
    for obj in all_objs:
        t = templates.EditablePaths(obj)
        objects.append(t)
    return templates.templates.TemplateResponse(
        "pages/edit.jinja",
        {
            "request": request,
            "objects": objects,
            "new_object": templates.NewPath(),
            "edit_on": ALLOW_EDITING_VIA_FORMS,
        },
    )


###############################################################################
# EDIT
# Below are the routes for read, update, delete actions via forms


@router.get("/assumptions", response_class=HTMLResponse)
async def form_assumptions(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return render_assumptions(request, db)


@router.get("/scenarios", response_class=HTMLResponse)
async def form_scenarios(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return render_scenarios(request, db)


@router.get("/runs", response_class=HTMLResponse)
async def form_runs(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return render_runs(request, db)


@router.get("/timeseries", response_class=HTMLResponse)
async def form_timeseries(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return render_timeseries(request, db)


@router.get("/paths", response_class=HTMLResponse)
async def form_paths(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return render_paths(request, db)


###############################################################################
# BELOW HERE, THE ROUTES ARE NOT ALWAYS AVAILABLE

###############################################################################
# CREATE
# Below are the create for read actions via forms


async def form_assumptions_create(
    request: Request,
    name: str = Form(...),
    kind: str = Form(...),
    detail: str = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # Make sure the assumption doesn't already exists
    existing = crud.assumptions.read(db=db, kind=kind, name=name)
    if existing:
        logger.info("assumption already exists")
        return RedirectResponse(request.url_for("form_assumptions"), status_code=302)
    else:
        try:
            crud.assumptions.create(name=name, kind=kind, detail=detail, db=db)
        except errors.DuplicateAssumptionError:
            logger.error("duplicate assumption given, no new object made")
        return RedirectResponse(request.url_for("form_assumptions"), status_code=302)


###############################################################################
# UPDATE
# Below are the create for read actions via forms


async def form_assumptions_update(
    request: Request,
    id: int = Form(...),
    name: str = Form(...),
    kind: str = Form(...),
    detail: str = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # Make sure the assumption doesn't already exists
    existing = crud.assumptions.read(db=db, id=id)
    if existing and (len(existing) == 1):
        logger.info(f"updating assumption {id=}, new data: {name=}, {kind=}, {detail=}")
        crud.assumptions.update(db, id=id, name=name, kind=kind, detail=detail)
        return RedirectResponse(request.url_for("form_assumptions"), status_code=302)
    else:
        logger.error("couldn't find assumption, no update made")
        return RedirectResponse(request.url_for("form_assumptions"), status_code=302)


async def form_scenarios_update(
    request: Request,
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # unpack to form data
    regular_attrs = {"name": str, "preferred_run": str, "id": int}
    kwargs = dict(assumptions=dict())
    form = await request.form()
    for attr, value in form.items():
        if attr in regular_attrs:
            factory = regular_attrs[attr]  # Get type/constructor
            kwargs[attr] = factory(value)  # Cast from str
        else:
            kwargs["assumptions"][attr] = value
    # Make sure the scenario doesn't already exists
    existing = crud.scenarios.read(db=db, id=kwargs["id"])
    if existing and (len(existing) == 1):
        logger.info(f"updating scenario {kwargs['id']=}, new data: {kwargs}")
        crud.scenarios.update(db, **kwargs)
        return RedirectResponse(request.url_for("form_scenarios"), status_code=302)
    else:
        logger.error("couldn't find scenario, no update made")
        return RedirectResponse(request.url_for("form_scenarios"), status_code=302)


async def form_runs_update(
    request: Request,
    scenario: str = Form(...),
    version: str = Form(...),
    contact: str = Form(...),
    # default to False because false switches don't get submitted with forms
    confidential: bool = Form(default=False),
    published: bool = Form(default=False),
    code_version: str = Form(...),
    detail: str = Form(...),
    id: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # Make sure the run doesn't already exists
    existing = crud.runs.read(db=db, id=id)
    if existing and (len(existing) == 1):
        logger.info(f"updating run {id=}")
        crud.runs.update(
            db,
            id=id,
            contact=contact,
            confidential=confidential,
            published=published,
            code_version=code_version,
            detail=detail,
        )
        return RedirectResponse(request.url_for("form_runs"), status_code=302)
    else:
        logger.error("couldn't find run, no update made")
        return RedirectResponse(request.url_for("form_runs"), status_code=302)


async def form_paths_update(
    request: Request,
    name: str = Form(...),
    path: str = Form(...),
    category: str = Form(...),
    period_type: str = Form(...),
    interval: str = Form(...),
    units: str = Form(...),
    detail: str = Form(...),
    id: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # Make sure the path doesn't already exists
    existing = crud.paths.read(db=db, id=id)
    if existing and (len(existing) == 1):
        logger.info(f"updating path {id=}")
        crud.paths.update(
            db,
            id=id,
            name=name,
            path=path,
            category=category,
            period_type=period_type,
            interval=interval,
            units=units,
            detail=detail,
        )
        return RedirectResponse(request.url_for("form_paths"), status_code=302)
    else:
        logger.error("couldn't find path, no update made")
        return RedirectResponse(request.url_for("form_paths"), status_code=302)


###############################################################################
# DELETE
# Below are the create for read actions via forms


async def form_assumptions_delete(
    request: Request,
    id: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    existing = crud.assumptions.read(db=db, id=id)
    if existing and (len(existing) == 1):
        crud.assumptions.delete(db=db, id=existing[0].id)
    else:
        logger.error("couldn't find assumption to delete.")
    return RedirectResponse(request.url_for("form_assumptions"), status_code=302)


async def form_scenarios_delete(
    request: Request,
    id: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    existing = crud.scenarios.read(db=db, id=id)
    if existing and (len(existing) == 1):
        crud.scenarios.delete(db=db, id=existing[0].id)
    else:
        logger.error("couldn't find scenario to delete.")
    return RedirectResponse(request.url_for("form_scenarios"), status_code=302)


async def form_runs_delete(
    request: Request,
    id: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    existing = crud.runs.read(db=db, id=id)
    if existing and (len(existing) == 1):
        crud.runs.delete(db=db, id=existing[0].id)
    else:
        logger.error("couldn't find run to delete.")
    return RedirectResponse(request.url_for("form_runs"), status_code=302)


async def form_paths_delete(
    request: Request,
    id: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    existing = crud.paths.read(db=db, id=id)
    if existing and (len(existing) == 1):
        crud.paths.delete(db=db, id=existing[0].id)
    else:
        logger.error("couldn't find path to delete.")
    return RedirectResponse(request.url_for("form_paths"), status_code=302)


if ALLOW_EDITING_VIA_FORMS:
    # Assumptions
    router.post(
        "/assumptions/create",
        response_class=RedirectResponse,
    )(form_assumptions_create)
    router.post(
        "/assumptions/update",
        response_class=RedirectResponse,
    )(form_assumptions_update)
    router.post(
        "/assumptions/delete",
        response_class=RedirectResponse,
    )(form_assumptions_delete)

    # Scenarios
    # router.post(
    #    "/scenarios/create",
    #    response_class=RedirectResponse,
    # (form_scenarios_create)
    router.post(
        "/scenarios/update",
        response_class=RedirectResponse,
    )(form_scenarios_update)
    router.post(
        "/scenarios/delete",
        response_class=RedirectResponse,
    )(form_scenarios_delete)

    # Runs
    # router.post(
    #    "/runs/create",
    #    response_class=RedirectResponse,
    # (form_runs_create)
    router.post(
        "/runs/update",
        response_class=RedirectResponse,
    )(form_runs_update)
    router.post(
        "/runs/delete",
        response_class=RedirectResponse,
    )(form_runs_delete)

    # Paths
    # router.post(
    #    "/paths/create",
    #    response_class=RedirectResponse,
    # (form_paths_create)
    router.post(
        "/paths/update",
        response_class=RedirectResponse,
    )(form_paths_update)
    router.post(
        "/paths/delete",
        response_class=RedirectResponse,
    )(form_paths_delete)
