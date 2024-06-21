from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..logger import logger
from ..schemas import CSRS_Model
from ..templates import templates

router = APIRouter(prefix="/forms", include_in_schema=False)


class EditableAttribute:
    def __init__(self, attr: str, value: str, id: str, kind: str = "input"):
        self.attr = attr
        self.value = value
        self.id = id
        self.kind = kind


class LongAttribute(EditableAttribute):
    def __init__(self, attr: str, value: str, id: str):
        super().__init__(attr, value, id, "textarea")


class SelectedAttribute(EditableAttribute):
    def __init__(self, attr: str, value: str, id: str, options: list):
        super().__init__(attr, value, id, "select")
        self.options = options


class TemplateObject:
    def __init__(
        self,
        attrs: list[EditableAttribute],
        title: str,
        id: str,
    ):
        self.attrs = attrs
        self.title = title
        self.id = id

    def __iter__(self):
        for attr in self.attrs:
            yield attr


@router.get("/test", response_class=HTMLResponse)
async def test(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    all_objs = crud.assumptions.read(db=db)
    all_kinds = crud.assumptions.read_kinds(db=db)
    template_objects = list()
    for obj in all_objs:
        t = TemplateObject(
            attrs=[
                EditableAttribute("name", obj.name, f"assumption-{obj.id}"),
                SelectedAttribute("kind", obj.kind, f"assumption-{obj.id}", all_kinds),
                LongAttribute("detail", obj.detail, f"assumption-{obj.id}"),
            ],
            title=obj.name,
            id=f"assumption-{obj.id}",
        )
        template_objects.append(t)
    return templates.TemplateResponse(
        "test.jinja",
        {
            "request": request,
            "objects": template_objects,
        },
    )


###############################################################################
# CREATE
# Below are the create for read actions via forms


@router.get("/assumptions/create", response_class=HTMLResponse)
async def create_assumption_form_get(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    kinds = crud.assumptions.read_kinds(db=db)
    sections = [
        SingleLineEntry("Name", attr="name"),
        OptionEntry("Kind", kinds, attr="kind"),
        MultiLineEntry("Detail", attr="detail"),
    ]
    return templates.TemplateResponse(
        "create.jinja",
        {
            "request": request,
            "page_label": "Assumptions",
            "sections": sections,
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
        sections = [
            SingleLineEntry("Name", attr="name"),
            SingleLineEntry("Kind", attr="kind"),
            MultiLineEntry("Detail", attr="detail"),
        ]
        return templates.TemplateResponse(
            "create.jinja",
            {
                "request": request,
                "error_message": "That Assumption already exists!",
                "page_label": "Assumptions",
                "sections": sections,
            },
        )
    else:
        crud.assumptions.create(name=name, kind=kind, detail=detail, db=db)
        return RedirectResponse(router.prefix + "/assumptions/read", status_code=302)


###############################################################################
# EDIT
# Below are the routes for read, update, delete actions via forms


@router.get("/edit/assumptions", response_class=HTMLResponse)
async def delete_assumption_form_get(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    all_objs = crud.assumptions.read(db=db)
    all_kinds = crud.assumptions.read_kinds(db=db)
    template_objects = list()
    for obj in all_objs:
        t = TemplateObject(
            attrs=[
                EditableAttribute("name", obj.name, f"assumption-{obj.id}"),
                SelectedAttribute("kind", obj.kind, f"assumption-{obj.id}", all_kinds),
                LongAttribute("detail", obj.detail, f"assumption-{obj.id}"),
            ],
            title=obj.name,
            id=f"assumption-{obj.id}",
        )
        template_objects.append(t)
    return templates.TemplateResponse(
        "test.jinja",
        {
            "request": request,
            "page_title": "Edit Assumptions",
            "objects": template_objects,
        },
    )


###############################################################################
# UPDATE
# Below are the routes for read, update, delete actions via forms
@router.post("/update/assumptions", response_class=HTMLResponse)
async def delete_assumption_form_get(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    all_objs = crud.assumptions.read(db=db)
    all_kinds = crud.assumptions.read_kinds(db=db)
    template_objects = list()
    for obj in all_objs:
        t = TemplateObject(
            attrs=[
                EditableAttribute("name", obj.name, f"assumption-{obj.id}"),
                SelectedAttribute("kind", obj.kind, f"assumption-{obj.id}", all_kinds),
                LongAttribute("detail", obj.detail, f"assumption-{obj.id}"),
            ],
            title=obj.name,
            id=f"assumption-{obj.id}",
        )
        template_objects.append(t)
    return templates.TemplateResponse(
        "test.jinja",
        {
            "request": request,
            "page_title": "Edit Assumptions",
            "objects": template_objects,
        },
    )
