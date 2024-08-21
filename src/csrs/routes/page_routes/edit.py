import logging

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from ... import crud, errors
from ...database import db_cfg, get_db
from ...pages import edit

router = APIRouter(prefix="/edit", include_in_schema=False)
logger = logging.getLogger(__name__)

###############################################################################
# EDIT
# Below are the routes for read, update, delete actions via forms


@router.get("/assumptions", response_class=HTMLResponse)
async def page_assumptions(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return edit.render_assumptions(request, db)


@router.get("/scenarios", response_class=HTMLResponse)
async def page_scenarios(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return edit.render_scenarios(request, db)


@router.get("/runs", response_class=HTMLResponse)
async def page_runs(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return edit.render_runs(request, db)


@router.get("/paths", response_class=HTMLResponse)
async def page_paths(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return edit.render_paths(request, db)


###############################################################################
# CREATE
# Below are the create for read actions via forms


async def page_assumptions_create(
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
        return RedirectResponse(request.url_for("page_assumptions"), status_code=302)
    else:
        try:
            crud.assumptions.create(name=name, kind=kind, detail=detail, db=db)
        except errors.DuplicateModelError:
            logger.error("duplicate assumption given, no new object made")
        return RedirectResponse(request.url_for("page_assumptions"), status_code=302)


async def page_scearios_create(
    request: Request,
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # unpack to form data
    regular_attrs = {"name": str, "id": int}
    kwargs = dict(assumptions=dict())
    form = await request.form()
    for attr, value in form.items():
        if attr in regular_attrs:
            factory = regular_attrs[attr]  # Get type/constructor
            kwargs[attr] = factory(value)  # Cast from str
        else:
            kwargs["assumptions"][attr] = value
    kwargs.pop("id", None)  # don't specify id when creating a new object
    # Make sure the scenario doesn't already exists
    existing = crud.scenarios.read(db=db, name=kwargs["name"])
    if existing:
        logger.info("scenario already exists")
        return RedirectResponse(request.url_for("page_scenarios"), status_code=302)
    else:
        try:
            crud.scenarios.create(db=db, **kwargs)
        except errors.DuplicateModelError:
            logger.error("duplicate scenario given, no new object made")
        return RedirectResponse(request.url_for("page_scenarios"), status_code=302)


async def page_runs_create(
    request: Request,
    scenario: str = Form(...),
    version: str = Form(...),
    parent: str = Form(default=None),
    contact: str = Form(...),
    # default to False because false switches don't get submitted with forms
    confidential: bool = Form(default=False),
    published: bool = Form(default=False),
    code_version: str = Form(...),
    detail: str = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # Make sure the run doesn't already exists
    existing = crud.runs.read(db=db, scenario=scenario, version=version)
    if existing:
        logger.info("run already exists")
        return RedirectResponse(request.url_for("page_runs"), status_code=302)
    else:
        try:
            crud.runs.create(
                db=db,
                scenario=scenario,
                version=version,
                parent=parent,
                contact=contact,
                confidential=confidential,
                published=published,
                code_version=code_version,
                detail=detail,
            )
        except errors.DuplicateModelError:
            logger.error("duplicate run given, no new object made")
        except AttributeError as e:
            logger.error(f"{e}")
        return RedirectResponse(request.url_for("page_runs"), status_code=302)


async def page_paths_create(
    request: Request,
    name: str = Form(...),
    path: str = Form(...),
    category: str = Form(...),
    period_type: str = Form(...),
    interval: str = Form(...),
    units: str = Form(...),
    detail: str = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # Make sure the path doesn't already exists
    existing = crud.paths.read(db=db, name=name, path=path)
    if existing:
        logger.info("path already exists")
        return RedirectResponse(request.url_for("page_paths"), status_code=302)
    else:
        try:
            crud.paths.create(
                db=db,
                name=name,
                path=path,
                category=category,
                period_type=period_type,
                interval=interval,
                units=units,
                detail=detail,
            )
        except errors.DuplicateModelError:
            logger.error("duplicate path given, no new object made")
        except AttributeError as e:
            logger.error(f"{e}")
        return RedirectResponse(request.url_for("page_paths"), status_code=302)


###############################################################################
# UPDATE
# Below are the create for read actions via forms


async def page_assumptions_update(
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
        return RedirectResponse(request.url_for("page_assumptions"), status_code=302)
    else:
        logger.error("couldn't find assumption, no update made")
        return RedirectResponse(request.url_for("page_assumptions"), status_code=302)


async def page_scenarios_update(
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
        return RedirectResponse(request.url_for("page_scenarios"), status_code=302)
    else:
        logger.error("couldn't find scenario, no update made")
        return RedirectResponse(request.url_for("page_scenarios"), status_code=302)


async def page_runs_update(
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
        return RedirectResponse(request.url_for("page_runs"), status_code=302)
    else:
        logger.error("couldn't find run, no update made")
        return RedirectResponse(request.url_for("page_runs"), status_code=302)


async def page_paths_update(
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
        return RedirectResponse(request.url_for("page_paths"), status_code=302)
    else:
        logger.error("couldn't find path, no update made")
        return RedirectResponse(request.url_for("page_paths"), status_code=302)


###############################################################################
# DELETE
# Below are the create for read actions via forms


async def page_assumptions_delete(
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
    return RedirectResponse(request.url_for("page_assumptions"), status_code=302)


async def page_scenarios_delete(
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
    return RedirectResponse(request.url_for("page_scenarios"), status_code=302)


async def page_runs_delete(
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
    return RedirectResponse(request.url_for("page_runs"), status_code=302)


async def page_paths_delete(
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
    return RedirectResponse(request.url_for("page_paths"), status_code=302)


if db_cfg.allow_editing_via_forms:
    # Assumptions
    router.post(
        "/assumptions/create",
        response_class=RedirectResponse,
    )(page_assumptions_create)
    router.post(
        "/assumptions/update",
        response_class=RedirectResponse,
    )(page_assumptions_update)
    router.post(
        "/assumptions/delete",
        response_class=RedirectResponse,
    )(page_assumptions_delete)

    # Scenarios
    router.post(
        "/scenarios/create",
        response_class=RedirectResponse,
    )(page_scearios_create)
    router.post(
        "/scenarios/update",
        response_class=RedirectResponse,
    )(page_scenarios_update)
    router.post(
        "/scenarios/delete",
        response_class=RedirectResponse,
    )(page_scenarios_delete)

    # Runs
    router.post(
        "/runs/create",
        response_class=RedirectResponse,
    )(page_runs_create)
    router.post(
        "/runs/update",
        response_class=RedirectResponse,
    )(page_runs_update)
    router.post(
        "/runs/delete",
        response_class=RedirectResponse,
    )(page_runs_delete)

    # Paths
    router.post(
        "/paths/create",
        response_class=RedirectResponse,
    )(page_paths_create)
    router.post(
        "/paths/update",
        response_class=RedirectResponse,
    )(page_paths_update)
    router.post(
        "/paths/delete",
        response_class=RedirectResponse,
    )(page_paths_delete)
