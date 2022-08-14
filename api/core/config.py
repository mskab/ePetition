import os
import urllib

from dotenv import load_dotenv
import os


load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(
                        os.path.abspath(__file__)
                        ))), ".env"
    )
)


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

    SECRET_KEY = str(os.environ.get("SECRET_KEY"))
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    TEST_EMAIL = "test_random_email@tre.com"


settings = Settings()
