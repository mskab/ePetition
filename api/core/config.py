import os
import urllib
from pathlib import Path

from dotenv import load_dotenv

env_path = Path("../") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "ePetition"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER")
    POSTGRES_PORT: str = urllib.parse.quote_plus(
        str(os.environ.get("POSTGRES_PORT"))
    )
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_USER = urllib.parse.quote_plus(
        str(os.environ.get("POSTGRES_USER"))
    )
    POSTGRES_PASSWORD = urllib.parse.quote_plus(
        str(os.environ.get("POSTGRES_PASSWORD"))
    )
    SSL_MODE = urllib.parse.quote_plus(str(os.environ.get("SSL_MODE")))
    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode={SSL_MODE}"
    )

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7


settings = Settings()
