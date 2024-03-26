from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.response.paths import PathModel
from ..models.sql import Path, Run, TimeSeriesValue

router = APIRouter(prefix="/paths")


@router.get("/", response_model=list[PathModel])
async def get_all_paths(scenario_id: int = None, db: Session = Depends(get_db)):
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


@router.post("/", response_model=PathModel)
async def post_path(path_data: PathModel, db: Session = Depends(get_db)):
    try:
        # Create a new Path object
        new_path = Path(**path_data.model_dump())

        # Add the new path to the database session
        db.add(new_path)
        db.commit()
        db.refresh(new_path)

        return path_data

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
