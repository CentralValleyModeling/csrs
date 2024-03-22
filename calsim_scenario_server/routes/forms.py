from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..logger import logger
from ..models import TUCP, VA, LandUse
from . import get_db

router = APIRouter(prefix="/forms")
templates = Jinja2Templates(directory="calsim_scenario_server/templates")


@router.get("/tucp", response_class=HTMLResponse)
async def get_tucp_form(request: Request, db: Session = Depends(get_db)):
    assumptions = db.query(TUCP).all()

    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project_type": "TUCP",
            "existing_assumptions": assumptions,
        },
    )


@router.post("/tucp")
async def post_tucp_form(detail: str = Form(...), db: Session = Depends(get_db)):
    logger.info(f"adding tucp assumption {detail=}")
    try:
        row = TUCP(detail=detail)
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {"message": "Assumption added", "detail": detail}

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/va", response_class=HTMLResponse)
async def get_va_form(request: Request, db: Session = Depends(get_db)):
    assumptions = db.query(VA).all()

    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project_type": "VA",
            "existing_assumptions": assumptions,
        },
    )


@router.post("/va")
async def post_va_form(detail: str = Form(...), db: Session = Depends(get_db)):
    logger.info(f"adding va assumption {detail=}")
    try:
        row = VA(detail=detail)
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {"message": "Assumption added", "detail": detail}

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
