from typing import Generator

from api.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def get_db() -> Generator:
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()
