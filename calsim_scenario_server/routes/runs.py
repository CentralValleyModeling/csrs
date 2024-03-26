from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..logger import logger
from ..models.response.runs import RunFullMetadata, RunShortMetadata, RunSubmission
from ..models.sql import Run, RunMetadata, Scenario

router = APIRouter(prefix="/runs")


def assert_scenario_exists(s_id: int | None, db: Session):
    if s_id is not None:
        s_count = db.query(Scenario).filter(Scenario.id == s_id).count()
        if s_count != 1:
            logger.error(f"scenario_id was not found, {s_id=}")
            raise HTTPException(
                status_code=400,
                detail=f"scenario_id={s_id} not found, you need to add it first",
            )


@router.get("/", response_model=list[RunShortMetadata])
async def get_all_runs(db: Session = Depends(get_db)):
    runs = db.query(Run).join(RunMetadata, Run.id == RunMetadata.run_id).all()
    if runs is None:
        raise HTTPException(status_code=404, detail="Runs not found")
    logger.info(f"{runs=}")
    return [RunShortMetadata(r.name, r.version, r.detail) for r in runs]


@router.get("/{run_id}", response_model=RunFullMetadata)
async def get_run(run_id: int, db: Session = Depends(get_db)):
    # TODO, this query will probably not work without changing column names
    run = (
        db.query(Run)
        .filter(Run.id == run_id)
        .join(RunMetadata, Run.id == RunMetadata.run_id)
        .join(Scenario, Run.scenario_id == Scenario.id)
        .join(Run, RunMetadata.predecessor_run_id == Run.id)
        .first()
    )
    if run is None:
        raise HTTPException(status_code=404, detail="Runs not found")
    logger.info(f"{run=}")
    return RunFullMetadata(
        name=run.name,
        version=run.version,
        predecessor_run=run.predecessor_run,
        contact=run.contact,
        confidential=run.confidential,
        published=run.published,
        code_version=run.code_version,
        detail=run.detail,
        scenario=run.scenario,
    )


@router.post("/", response_model=RunSubmission)
async def post_run(run_data: RunSubmission, db: Session = Depends(get_db)):
    logger.info(run_data)
    try:
        assert_scenario_exists(run_data.scenario_id, db)
        assert_scenario_exists(run_data.predecessor_run_id, db)
        metadata = {
            "contact",
            "confidential",
            "published",
            "code_version",
            "detail",
            "predecessor_run_id",
        }
        # Create a new Path object
        new_run = Run(**run_data.model_dump(exclude=metadata))
        new_run_metadata = RunMetadata(**run_data.model_dump(include=metadata))

        # Add the new path to the database session
        db.add(new_run)
        db.add(new_run_metadata)
        db.commit()
        db.refresh(new_run)
        db.refresh(new_run_metadata)

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        logger.error(f"{type(e)} encountered: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return run_data
