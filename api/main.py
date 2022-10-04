# pylint: skip-file
import os

os.chdir(os.getcwd() + '/api')

from api.core.config import settings
from api.db.base import Base
from api.db.session import engine
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from api.routes.base import api_router
from api.schemas.jwt import TokenConfig


@AuthJWT.load_config
def get_config():
    return TokenConfig()


def include_router(app):
    app.include_router(api_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION
    )
    include_router(app)
    create_tables()
    return app


app = start_application()
