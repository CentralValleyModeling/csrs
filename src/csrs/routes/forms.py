from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..logger import logger
from ..templates import templates

router = APIRouter(prefix="/forms", include_in_schema=False)


@router.get("/assumptions/read", response_class=HTMLResponse)
async def get_assumption_form(request: Request, db: Session = Depends(get_db)):
    all_objs = crud.assumptions.read(db=db)
    cat = sorted(set(o.kind for o in all_objs))
    grouped = {k: {"label": k, "items": list()} for k in cat}
    for o in all_objs:
        grouped[o.kind]["items"].append(o)
    grouped = [v for v in grouped.values()]

    return templates.TemplateResponse(
        "read.jinja",
        {
            "request": request,
            "page_label": "Assumptions",
            "accordion_content": grouped,
            "attrs_to_display": ["name", "detail"],
            "action_links": ["create", "update", "delete"],
        },
    )


@router.get("/scenarios/read", response_class=HTMLResponse)
async def get_scenario_form(request: Request, db: Session = Depends(get_db)):
    objs = crud.scenarios.read(db=db)
    return templates.TemplateResponse(
        "read.jinja",
        {
            "request": request,
            "page_label": "Scenarios",
            "accordion_content": [{"items": objs}],
            "attrs_to_display": ["name", "assumptions", "preferred_run"],
            "action_links": ["create", "update", "delete"],
        },
    )


@router.get("/runs/read", response_class=HTMLResponse)
async def get_run_form(request: Request, db: Session = Depends(get_db)):
    all_objs = crud.runs.read(db=db)
    cat = sorted(set(o.scenario for o in all_objs))
    grouped = {k: {"label": k, "items": list()} for k in cat}
    for o in all_objs:
        grouped[o.scenario]["items"].append(o)
    grouped = [v for v in grouped.values()]

    return templates.TemplateResponse(
        "read.jinja",
        {
            "request": request,
            "page_label": "Runs",
            "accordion_content": grouped,
            "attrs_to_display": [
                "detail",
                "contact",
                "confidential",
                "published",
                "parent",
                "children",
            ],
            "action_links": ["create", "update", "delete"],
        },
    )


@router.get("/paths/read", response_class=HTMLResponse)
async def get_namedpath_form(request: Request, db: Session = Depends(get_db)):
    all_objs = crud.paths.read(db=db)
    cat = sorted(set(o.category for o in all_objs))
    grouped = {k: {"label": k, "items": list()} for k in cat}
    for o in all_objs:
        grouped[o.category]["items"].append(o)
    grouped = [v for v in grouped.values()]

    return templates.TemplateResponse(
        "read.jinja",
        {
            "request": request,
            "page_label": "Named Paths",
            "accordion_content": grouped,
            "attrs_to_display": [
                "name",
                "path",
                "detail",
                "units",
                "period_type",
                "interval",
            ],
            "action_links": ["create", "update", "delete"],
        },
    )


@router.get("/assumptions/create", response_class=HTMLResponse)
async def create_assumption_form_get(request: Request, db: Session = Depends(get_db)):
    kinds = crud.assumptions.read_kinds(db=db)
    attrs = [
        {"kind": "input", "name": "name"},
        {"kind": "select", "name": "kind", "options": kinds},
        {"kind": "textarea", "name": "detail"},
    ]
    return templates.TemplateResponse(
        "create.jinja",
        {
            "request": request,
            "page_label": "Assumptions",
            "action_links": ["read", "update", "delete"],
            "attrs": attrs,
        },
    )


@router.post("/assumptions/create", response_class=RedirectResponse)
async def create_assumption_form_put(
    request: Request,
    name: str = Form(...),
    kind: str = Form(...),
    detail: str = Form(...),
    db: Session = Depends(get_db),
):
    # Make sure the assumption doesn't already exists
    existing = crud.assumptions.read(db=db, kind=kind, name=name)
    if existing:
        kinds = crud.assumptions.read_kinds(db=db)
        attrs = [
            {"kind": "input", "name": "name", "value": name},
            {"kind": "select", "name": "kind", "options": kinds, "value": kind},
            {"kind": "textarea", "name": "detail", "label": "Detail", "value": detail},
        ]
        return templates.TemplateResponse(
            "create.jinja",
            {
                "error_message": "That 'kind' and 'name' combination already exists!",
                "request": request,
                "page_label": "Assumptions",
                "action_links": ["read", "update", "delete"],
                "attrs": attrs,
            },
        )
    else:
        # Add the new data
        return RedirectResponse(router.prefix + "/assumptions/read", status_code=302)


@router.get("/assumptions/delete", response_class=HTMLResponse)
async def delete_assumption_form_get(request: Request, db: Session = Depends(get_db)):
    objs = crud.assumptions.read(db=db)
    objs = sorted([f"{o.kind} - {o.name}" for o in objs])
    return templates.TemplateResponse(
        "delete.jinja",
        {
            "request": request,
            "page_label": "Assumptions",
            "action_links": ["read", "create", "update"],
            "options": objs,
        },
    )
