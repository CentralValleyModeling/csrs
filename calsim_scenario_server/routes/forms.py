from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..logger import logger
from ..models import (
    AssumptionDeltaConveyanceProject,
    AssumptionHydrology,
    AssumptionLandUse,
    AssumptionSeaLevelRise,
    AssumptionSouthOfDeltaStorage,
    AssumptionTUCP,
    AssumptionVoluntaryAgreements,
    Scenario,
)
from . import get_db

router = APIRouter(prefix="/forms")
templates = Jinja2Templates(directory="calsim_scenario_server/templates")


@router.get("/scenarios", response_class=HTMLResponse)
async def get_scenario_form(request: Request, db: Session = Depends(get_db)):
    scenarios = db.query(Scenario).all()
    # The keys to this dict will be converted to ids in the HTML,
    # those ids should be valid python vars, because they are what FastAPI
    # passes to the POST request handler
    assumption_tables = {
        "Hydrology": AssumptionHydrology,
        "Sea Level Rise": AssumptionSeaLevelRise,
        "Land Use": AssumptionLandUse,
        "TUCP": AssumptionTUCP,
        "DCP": AssumptionDeltaConveyanceProject,
        "VA": AssumptionVoluntaryAgreements,
        "South of Delta Storage": AssumptionSouthOfDeltaStorage,
    }

    existing_assumptions = {
        k: db.query(tbl).all() for k, tbl in assumption_tables.items()
    }

    return templates.TemplateResponse(
        "scenario.html",
        {
            "request": request,
            "scenarios": scenarios,
            "existing_assumptions": existing_assumptions,
        },
    )


@router.post("/scenarios")
async def post_scenario_form(
    scenario_name: str = Form(...),
    hydrology: int = Form(...),
    sea_level_rise: int = Form(...),
    land_use: int = Form(...),
    tucp: int = Form(...),
    dcp: int = Form(...),
    va: int = Form(...),
    south_of_delta_storage: int = Form(...),
    db: Session = Depends(get_db),
):
    logger.info(f"adding assumption {scenario_name=}")
    try:
        row = Scenario(
            scenario_name=scenario_name,
            hydrology_id=hydrology,
            sea_level_rise_id=sea_level_rise,
            land_use_id=land_use,
            tucp_id=tucp,
            dcp_id=dcp,
            va_id=va,
            sod_id=south_of_delta_storage,
        )
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {"message": "Assumption added", "scenario": row}

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tucp", response_class=HTMLResponse)
async def get_tucp_form(request: Request, db: Session = Depends(get_db)):
    assumptions = db.query(AssumptionTUCP).all()

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
        row = AssumptionTUCP(detail=detail)
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
    assumptions = db.query(AssumptionVoluntaryAgreements).all()

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
        row = AssumptionVoluntaryAgreements(detail=detail)
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {"message": "Assumption added", "detail": detail}

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hydrology", response_class=HTMLResponse)
async def get_hydrology_form(request: Request, db: Session = Depends(get_db)):
    assumptions = db.query(AssumptionHydrology).all()

    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project_type": "Hydrology",
            "existing_assumptions": assumptions,
        },
    )


@router.post("/hydrology")
async def post_hydrology_form(detail: str = Form(...), db: Session = Depends(get_db)):
    logger.info(f"adding assumption {detail=}")
    try:
        row = AssumptionHydrology(detail=detail)
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {"message": "Assumption added", "detail": detail}

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dcp", response_class=HTMLResponse)
async def get_dcp_form(request: Request, db: Session = Depends(get_db)):
    assumptions = db.query(AssumptionDeltaConveyanceProject).all()

    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project_type": "DCP",
            "existing_assumptions": assumptions,
        },
    )


@router.post("/dcp")
async def post_dcp_form(detail: str = Form(...), db: Session = Depends(get_db)):
    logger.info(f"adding assumption {detail=}")
    try:
        row = AssumptionDeltaConveyanceProject(detail=detail)
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {"message": "Assumption added", "detail": detail}

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/south_of_delta_storage", response_class=HTMLResponse)
async def get_sod_form(request: Request, db: Session = Depends(get_db)):
    assumptions = db.query(AssumptionSouthOfDeltaStorage).all()

    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project_type": "South of Delta Storage",
            "existing_assumptions": assumptions,
        },
    )


@router.post("/south_of_delta_storage")
async def post_sod_form(detail: str = Form(...), db: Session = Depends(get_db)):
    logger.info(f"adding assumption {detail=}")
    try:
        row = AssumptionSouthOfDeltaStorage(detail=detail)
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
    assumptions = db.query(AssumptionLandUse).all()

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
        row = AssumptionLandUse(detail=detail, future_year=future_year)
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
    assumptions = db.query(AssumptionSeaLevelRise).all()

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
        row = AssumptionSeaLevelRise(detail=detail, centimeters=centimeters)
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
