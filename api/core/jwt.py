import datetime
from fastapi_jwt_auth import AuthJWT
from core.config import settings


def create_access_token(subject: str, Auth: AuthJWT):
    return Auth.create_access_token(
        subject=subject,
        expires_time=datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        algorithm=settings.ALGORITHM
    )


def create_refresh_token(subject: str, Auth: AuthJWT):
    return Auth.create_refresh_token(
        subject=subject,
        expires_time=datetime.timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        algorithm=settings.ALGORITHM
    )
