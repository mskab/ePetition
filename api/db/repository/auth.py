from api.core.hashing import Hasher
from api.db.models.user import User
from api.db.repository import user
from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session


def authenticate_user(_db: Session, email: str, password: str):
    db_user: User = user.get_by_email(_db, email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email does not exist",
        )

    if db_user.is_active:
        if not Hasher.verify_password(password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password does not match the email provided",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account is inactive",
        )
    return db_user


def get_authenteficated_user(_db: Session, Auth: AuthJWT):
    Auth.jwt_required()
    email = Auth.get_jwt_subject()
    current_user: User = user.get_by_email(_db, email)
    return current_user


def is_only_admin_permitted(_db: Session, Auth: AuthJWT):
    current_user = get_authenteficated_user(_db, Auth)
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def is_only_user_permitted(_db: Session, Auth: AuthJWT):
    current_user = get_authenteficated_user(_db, Auth)
    if current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
