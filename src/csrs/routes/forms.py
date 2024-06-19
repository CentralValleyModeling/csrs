from pprint import pformat

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..logger import logger
from ..schemas import CSRS_Model
from ..templates import templates

router = APIRouter(prefix="/forms", include_in_schema=False)


class AccordionSection:
    def __init__(self, title: str, obj: object):
        self.title = title
        self.obj = obj

    def items(self):
        for a in self.iter_attrs():
            yield a, getattr(self.obj, a)

    def pitems(self):
        for k, v in self.items():
            yield k, pformat(v, indent=4, compact=True).strip("'")

    def iter_attrs(self):
        if isinstance(self.obj, CSRS_Model):
            yield from sorted(self.obj.model_fields_set)
        else:
            for a in dir(self.obj):
                if a.startswith("_") or callable(getattr(self.obj, a)):
                    yield a

    @property
    def panel_id(self):
        return self.title.lower().replace(" ", "-").split("\n")[0]


class Accordion:
    def __init__(
        self,
        header: str,
        sections: dict[str, object],
    ):
        self.header = header
        # Convert to AccordionSection
        clean: dict[str, AccordionSection] = dict()
        for title, section in sections.items():
            if not isinstance(section, AccordionSection):
                section = AccordionSection(title=title, obj=section)
            clean[title] = section
        self.sections = clean

    def __iter__(self):
        yield from self.sections

    def items(self):
        yield from self.sections.items()

    @property
    def panel_id(self):
        return self.header.lower().replace(" ", "-").split("\n")[0]


###############################################################################
# READ
# Below are the routes for read actions via forms


@router.get("/assumptions/read", response_class=HTMLResponse)
async def get_assumption_form(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    all_objs = crud.assumptions.read(db=db)
    categorized: dict[str, list[AccordionSection]] = dict()
    for obj in all_objs:
        section = AccordionSection(title=obj.name, obj=obj)
        if obj.kind not in categorized:
            categorized[obj.kind] = dict()
        categorized[obj.kind][obj.name] = section
    accordions = [Accordion(k, v) for k, v in categorized.items()]

    return templates.TemplateResponse(
        "read.jinja",
        {
            "request": request,
            "page_label": "Assumptions",
            "accordions": accordions,
        },
    )


@router.get("/scenarios/read", response_class=HTMLResponse)
async def get_scenario_form(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    all_objs = crud.scenarios.read(db=db)
    categorized: dict[str, list[AccordionSection]] = {"All Active Scenarios": dict()}
    for obj in all_objs:
        section = AccordionSection(title=obj.name, obj=obj)
        categorized["All Active Scenarios"][obj.name] = section
    accordions = [Accordion(header=k, sections=v) for k, v in categorized.items()]
    return templates.TemplateResponse(
        "read.jinja",
        {
            "request": request,
            "page_label": "Scenarios",
            "accordions": accordions,
        },
    )


@router.get("/runs/read", response_class=HTMLResponse)
async def get_run_form(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    all_objs = crud.runs.read(db=db)
    categorized: dict[str, list[AccordionSection]] = dict()
    for obj in all_objs:
        section = AccordionSection(title=f"v{obj.version}", obj=obj)
        if obj.scenario not in categorized:
            categorized[obj.scenario] = dict()
        categorized[obj.scenario][obj.version] = section
    accordions = [Accordion(header=k, sections=v) for k, v in categorized.items()]

    return templates.TemplateResponse(
        "read.jinja",
        {
            "request": request,
            "page_label": "Assumptions",
            "accordions": accordions,
        },
    )


@router.get("/paths/read", response_class=HTMLResponse)
async def get_namedpath_form(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    all_objs = crud.paths.read(db=db)
    categorized: dict[str, list[AccordionSection]] = dict()
    for obj in all_objs:
        section = AccordionSection(title=obj.name, obj=obj)
        if obj.category not in categorized:
            categorized[obj.category] = dict()
        categorized[obj.category][obj.name] = section
    accordions = [Accordion(header=k, sections=v) for k, v in categorized.items()]

    return templates.TemplateResponse(
        "read.jinja",
        {
            "request": request,
            "page_label": "Assumptions",
            "accordions": accordions,
        },
    )


###############################################################################
# CREATE
# Below are the create for read actions via forms


@router.get("/assumptions/create", response_class=HTMLResponse)
async def create_assumption_form_get(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
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
    logger.info(f"{request.method} {request.url}")
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
                "attrs": attrs,
            },
        )
    else:
        # Add the new data
        return RedirectResponse(router.prefix + "/assumptions/read", status_code=302)


###############################################################################
# DELETE
# Below are the routes for delete actions via forms


@router.get("/assumptions/delete", response_class=HTMLResponse)
async def delete_assumption_form_get(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    objs = crud.assumptions.read(db=db)
    objs = sorted([f"{o.kind} - {o.name}" for o in objs])
    return templates.TemplateResponse(
        "delete.jinja",
        {
            "request": request,
            "page_label": "Assumptions",
            "options": objs,
        },
    )
