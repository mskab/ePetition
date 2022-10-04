# pylint: skip-file
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/core")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/db")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/routes")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/schemas")
#os.chdir(os.getcwd() + '/api')

from core.config import settings
from db.base import Base
from db.session import engine
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from routes.base import api_router
from schemas.jwt import TokenConfig


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
