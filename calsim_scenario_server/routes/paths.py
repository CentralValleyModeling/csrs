from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models.http.paths import PathModel
from ..models.sql import Path, Run, TimeSeriesValue

router = APIRouter(prefix="/paths", tags=["Paths"])


@router.get("/", response_model=list[PathModel])
async def get_all_paths(scenario_id: int = None, db: Session = Depends(get_db)):
    logger.info(f"getting all paths {scenario_id=}")
    if scenario_id:
        paths = (
            db.query(Path)
            .join(TimeSeriesValue, TimeSeriesValue.path_id == Path.path_id)
            .join(Run, Run.id == TimeSeriesValue.run_id)
            .filter(Run.scenario_id == scenario_id)
            .distinct()  # Ensure unique paths
            .all()
        )
    else:
        paths = db.query(Path).all()

    if paths is None:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return paths


@router.put("/", response_model=PathModel)
async def put_path(path_data: PathModel, db: Session = Depends(get_db)):
    logger.info(f"{path_data=}")
    try:
        # Create a new Path object
        new_path = Path(**path_data.model_dump())

        # Add the new path to the database session
        db.add(new_path)
        db.commit()
        db.refresh(new_path)

    except IntegrityError:
        logger.info(f"{path_data=} violates SQL rules")

    except Exception as e:
        logger.error(f"{type(e)}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return path_data
