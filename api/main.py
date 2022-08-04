from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.base import Base
from routes.base import api_router


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
