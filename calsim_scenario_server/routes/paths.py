from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models import NamedPathModel, RunModel, TimeSeriesModel
from ..schemas import NamedDatasetPath

router = APIRouter(prefix="/paths", tags=["Paths"])


@router.get("/", response_model=list[NamedDatasetPath])
async def get_all_paths(scenario_id: int = None, db: Session = Depends(get_db)):
    logger.info(f"getting all paths {scenario_id=}")
    if scenario_id:
        paths = (
            db.query(NamedPathModel)
            .join(
                TimeSeriesModel,
                TimeSeriesModel.path_id == NamedPathModel.path_id,
            )
            .join(RunModel, RunModel.id == TimeSeriesModel.run_id)
            .filter(RunModel.scenario_id == scenario_id)
            .distinct()  # Ensure unique paths
            .all()
        )
    else:
        paths = db.query(NamedPathModel).all()

    if paths is None:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return paths


@router.put("/", response_model=NamedDatasetPath)
async def put_path(path_data: NamedDatasetPath, db: Session = Depends(get_db)):
    logger.info(f"{path_data=}")
    try:
        # Create a new Path object
        new_path = NamedPathModel(**path_data.model_dump())

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
