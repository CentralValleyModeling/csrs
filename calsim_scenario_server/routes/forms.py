from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..logger import logger
from ..models import TUCP, VA, LandUse, SeaLevelRise
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
    logger.info(f"adding assumption {detail=}")
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
    logger.info(f"adding assumption {detail=}")
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


@router.get("/land_use", response_class=HTMLResponse)
async def get_land_use_form(request: Request, db: Session = Depends(get_db)):
    assumptions = db.query(LandUse).all()

    return templates.TemplateResponse(
        "project_land_use.html",
        {
            "request": request,
            "project_type": "Land Use",
            "existing_assumptions": assumptions,
        },
    )


@router.post("/land_use")
async def post_land_use_form(
    detail: str = Form(...),
    future_year: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"adding assumption {detail=}, {future_year=}")
    if int(future_year) < 2020:
        msg = f"future year entered not in the future: {future_year}"
        logger.error(msg)
        raise HTTPException(status_code=422, detail=msg)
    try:
        row = LandUse(detail=detail, future_year=future_year)
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {
            "message": "Assumption added",
            "detail": detail,
            "future_year": future_year,
        }

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sea_level_rise", response_class=HTMLResponse)
async def get_sea_level_rise_form(request: Request, db: Session = Depends(get_db)):
    assumptions = db.query(SeaLevelRise).all()

    return templates.TemplateResponse(
        "project_sea_level_rise.html",
        {
            "request": request,
            "project_type": "Sea Level Rise",
            "existing_assumptions": assumptions,
        },
    )


@router.post("/sea_level_rise")
async def post_sea_level_rise_form(
    detail: str = Form(...),
    centimeters: float = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"adding assumption {detail=}, {centimeters=}")
    try:
        row = SeaLevelRise(detail=detail, centimeters=centimeters)
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {
            "message": "Assumption added",
            "detail": detail,
            "centimeters": centimeters,
        }

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
