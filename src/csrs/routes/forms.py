from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import crud, errors
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
        db_id: int,
    ):
        self.attrs = attrs
        self.title = title
        self.id = id
        self.db_id = db_id

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
            db_id=obj.id,
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
# RENDER
# Below are page rendering functions


def render_assumptions(request: Request, db: Session):
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
            db_id=obj.id,
        )
        template_objects.append(t)
    new_t = TemplateObject(
        attrs=[
            EditableAttribute("name", "", "assumption-new"),
            SelectedAttribute("kind", "", "assumption-new", all_kinds),
            LongAttribute("detail", "", "assumption-new"),
        ],
        title="assumption-new",
        id="assumption-new",
        db_id=None,
    )
    return templates.TemplateResponse(
        "edit.jinja",
        {
            "request": request,
            "page_title": "Assumptions",
            "page_description": "Assumptions are used by Scenarios.",
            "new_object_template": new_t,
            "objects": template_objects,
        },
    )


###############################################################################
# CREATE
# Below are the create for read actions via forms


@router.post("/assumptions/create", response_class=RedirectResponse)
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


@router.post("/assumptions/update", response_class=RedirectResponse)
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


###############################################################################
# DELETE
# Below are the create for read actions via forms


@router.post("/assumptions/delete", response_class=RedirectResponse)
async def form_assumptions_delete(
    request: Request,
    name: str = Form(...),
    kind: str = Form(...),
    detail: str = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"{request.method} {request.url}")
    # Make sure the assumption doesn't already exists
    existing = crud.assumptions.read(db=db, kind=kind, name=name)
    if existing and (len(existing) == 1):
        crud.assumptions.delete(db=db, id=existing[0].id)
    else:
        logger.error("couldn't find assumption to delete.")

    return RedirectResponse(request.url_for("form_assumptions"), status_code=302)


###############################################################################
# EDIT
# Below are the routes for read, update, delete actions via forms


@router.get("/assumptions", response_class=HTMLResponse)
async def form_assumptions(request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    return render_assumptions(request, db)
