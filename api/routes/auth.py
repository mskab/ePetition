from core import jwt
from db.repository import auth
from db.session import get_db
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from schemas.jwt import TokenLogin, TokenRefresh
from sqlalchemy.orm import Session

router = APIRouter()

default_OAuth = Depends()
default_authJWT = Depends()
default_session = Depends(get_db)


@router.post("/login", response_model=TokenLogin)
def login_user(
    form_data: OAuth2PasswordRequestForm = default_OAuth,
    Auth: AuthJWT = default_authJWT,
    db: Session = default_session,
):
    user = auth.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    access_token = jwt.create_access_token(user.email, Auth)
    refresh_token = jwt.create_refresh_token(user.email, Auth)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/refresh", response_model=TokenRefresh)
def refresh(Auth: AuthJWT = default_authJWT):
    Auth.jwt_refresh_token_required()

    current_user = Auth.get_jwt_subject()
    new_access_token = jwt.create_access_token(current_user, Auth)

    return {"access_token": new_access_token}
