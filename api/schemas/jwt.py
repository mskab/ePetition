from core.config import settings
from pydantic import BaseModel


class TokenConfig(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY


class TokenLogin(BaseModel):
    access_token: str
    refresh_token: str


class TokenRefresh(BaseModel):
    access_token: str
