from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import assumptions
from ..database import get_db
from ..logger import logger
from ..models import AssumptionModel
from ..schemas import Assumption, Scenario

router = APIRouter(prefix="/assumptions", tags=["Assumptions"])


def build_reposne_from_model(model: AssumptionModel) -> Assumption:
    return Assumption(
        name=model.name,
        kind=model.kind,
        detail=model.detail,
        id=model.id,
    )


def verify_assumption_type(assumption_type: str):
    if assumption_type not in Scenario.model_fields:
        logger.error(f"invalid assumption type given: {assumption_type=}")
        raise HTTPException(
            status_code=400,
            detail=f"{assumption_type} not a recognized assumption table name, "
            + "the following names are recognized:"
            + "\n".join(map(str, Scenario.model_fields)),
        )


@router.get("", response_model=list[str])
async def get_assumption_table_names():
    return Scenario.get_assumption_attrs()


@router.get("/{assumption_type}", response_model=list[Assumption])
async def get_assumption(
    assumption_type: str,
    id: int = None,
    name: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"{assumption_type=}")
    verify_assumption_type(assumption_type)
    models = assumptions.read(db, id=id, name=name)
    logger.debug(f"{len(models)} assumptions found")
    for m in models:
        logger.debug(f"{m.name=}, {m.detail=}")
    return [build_reposne_from_model(m) for m in models]


@router.put(
    "/{assumption_type}",
    response_model=Assumption,
    responses={
        200: {"detail": "assumption added"},
        400: {"detail": "assumption not added"},
    },
)
async def put_assumption(
    assumption_type: str,
    assumption: Assumption,
    db: Session = Depends(get_db),
):
    logger.info(f"{assumption_type=}, {assumption=}")
    verify_assumption_type(assumption_type)
    model = assumptions.create(db=db, **assumption.model_dump(exclude=("id")))
    return build_reposne_from_model(model)
