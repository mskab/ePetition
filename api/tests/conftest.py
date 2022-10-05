from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import os
print("1---------------------",os.getcwd())
from sqlalchemy.orm import sessionmaker, Session
from utils.constants import USER_TEST_DATA
from utils.users import authentication_token_from_email, register_admin_to_db

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("2---------------------",os.getcwd())

from db.base import Base
from db.session import get_db
from routes.base import api_router
from fastapi_jwt_auth import AuthJWT
from schemas.jwt import TokenConfig


@AuthJWT.load_config
def get_config():
    return TokenConfig()

print("3---------------------",os.getcwd())
def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db_session: Session):
    return  authentication_token_from_email(
        client=client, email=USER_TEST_DATA["email"], db=db_session
    )


@pytest.fixture(scope="function")
def primary_admin_token_headers(client: TestClient, db_session: Session):
    return register_admin_to_db(client=client, db=db_session)
