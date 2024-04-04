from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..logger import logger
from ..schemas import AssumptionIn, AssumptionOut

router = APIRouter(prefix="/assumptions", tags=["Assumptions"])
TableNames = crud.assumptions.TableNames


def get_additional_metatada_from_model(model) -> dict:
    attrs = model.__table__.columns.keys()
    return {
        attr: getattr(model, attr)
        for attr in attrs
        if attr not in ("id", "name", "detail")
    }


def build_reposne_from_model(model) -> AssumptionOut:
    additional_metadata = get_additional_metatada_from_model(model)
    return AssumptionOut(
        name=model.name,
        detail=model.detail,
        id=model.id,
        additional_metadata=additional_metadata,
    )


def verify_assumption_type(assumption_type: str):
    if assumption_type not in TableNames:
        logger.error(f"invalid assumption type given: {assumption_type=}")
        raise HTTPException(
            status_code=400,
            detail=f"{assumption_type} not a recognized assumption table name, "
            + "the following names are recognized:"
            + "\n".join(map(str, list(TableNames))),
        )


@router.get("/{assumption_type}", response_model=list[AssumptionOut])
async def get_assumption(
    assumption_type: str,
    id: int = None,
    name: str = None,
    db: Session = Depends(get_db),
):
    logger.info(f"{assumption_type=}")
    verify_assumption_type(assumption_type)
    module = TableNames[assumption_type].value
    models = module.read(db, id=id, name=name)
    logger.info(f"{len(models)} assumptions found")
    for m in models:
        logger.debug(f"{m.name=}, {m.detail=}")
    return [build_reposne_from_model(m) for m in models]


@router.put(
    "/{assumption_type}",
    response_model=AssumptionOut,
    responses={
        200: {"detail": "assumption added"},
        400: {"detail": "assumption not added"},
    },
)
async def put_assumption(
    assumption_type: str,
    assumption: AssumptionIn,
    db: Session = Depends(get_db),
):
    logger.info(f"{assumption_type=}, {assumption=}")
    verify_assumption_type(assumption_type)

    module = TableNames[assumption_type].value
    model = module.create(
        name=assumption.name,
        detail=assumption.detail,
        db=db,
        **assumption.additional_metadata,
    )
    return build_reposne_from_model(model)
