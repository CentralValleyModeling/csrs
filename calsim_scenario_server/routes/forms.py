from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models import AssumptionModel, ScenarioModel

router = APIRouter(prefix="/forms")
templates = Jinja2Templates(directory="calsim_scenario_server/templates")


@router.get("/scenarios", response_class=HTMLResponse)
async def get_scenario_form(request: Request, db: Session = Depends(get_db)):
    scenarios = db.query(ScenarioModel).all()
    # The keys to this dict will be converted to ids in the HTML,
    # those ids should be valid python vars, because they are what FastAPI
    # passes to the PUT request handler
    assumption_tables = {
        "Hydrology": AssumptionModel,
        "Sea Level Rise": AssumptionModel,
        "Land Use": AssumptionModel,
        "TUCP": AssumptionModel,
        "DCP": AssumptionModel,
        "VA": AssumptionModel,
        "South of Delta Storage": AssumptionModel,
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


@router.put("/scenarios")
async def put_scenario_form(
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
        row = ScenarioModel(
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


@router.get("/{assumption_type}", response_class=HTMLResponse)
async def get_dcp_form(
    assumption_type: str, request: Request, db: Session = Depends(get_db)
):
    assumptions = db.query(AssumptionModel).filter(
        AssumptionModel.kind == assumption_type
    )

    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project_type": "DCP",
            "existing_assumptions": assumptions,
        },
    )


@router.put("/dcp")
async def put_dcp_form(detail: str = Form(...), db: Session = Depends(get_db)):
    logger.info(f"adding assumption {detail=}")
    try:
        row = AssumptionModel(detail=detail)
        # Add the new path to the database session
        db.add(row)
        db.commit()
        db.refresh(row)

        return {"message": "Assumption added", "detail": detail}

    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
