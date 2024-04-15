from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from calsim_scenario_server import crud, schemas
from calsim_scenario_server.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
session = TestingSessionLocal()


def test_create_assumpitons():
    kwargs = dict(
        name="testing-create-assumption",
        kind="tucp",
        detail="testing assumption, tucp as placeholder",
        db=session,
    )
    assumption = crud.assumptions.create(**kwargs)
    assert isinstance(assumption, schemas.Assumption)
    assert assumption.name == kwargs["name"]


def test_read_assumpitons():
    kwargs = dict(
        name="testing-create-assumption",
        kind="tucp",
        detail="testing assumption, tucp as placeholder",
        db=session,
    )
    crud.assumptions.create(**kwargs)
    assumptions = crud.assumptions.read(name=kwargs["name"], db=kwargs["db"])
    for assumption in assumptions:
        assert isinstance(assumption, schemas.Assumption)
        assert assumption.name == kwargs["name"]