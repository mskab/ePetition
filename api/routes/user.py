from typing import List, Union

from db.repository import auth, user
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from schemas.common import StatusResponse
from schemas.user import (
    UserCreate,
    UserInfo,
    UserInfoAllAllowedFields,
    UserUpdate,
    UserUpdateAllAllowedFields,
)
from sqlalchemy.orm import Session

router = APIRouter()
default_session = Depends(get_db)
default_authJWT = Depends()


@router.post(
    "/", response_model=UserInfo, status_code=status.HTTP_201_CREATED
)
def create_user(req_user: UserCreate, db: Session = default_session):
    """
    Create an User and store it in the database
    """
    return user.create(db, req_user)


@router.get("/", response_model=List[UserInfoAllAllowedFields])
def get_all_users(
    offset: int,
    limit: int,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Get all the Users stored in database
    """
    auth.is_only_admin_permitted(db, Auth)

    return user.get_all(db, offset, limit)


@router.get(
    "/{user_id}",
    response_model=Union[UserInfoAllAllowedFields, UserInfo],
)
def get_user(
    user_id: int,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Get the User with the given ID
    """
    current_user = auth.get_authenteficated_user(db, Auth)
    db_user = user.get_by_id(db, user_id)
    if current_user.is_admin:
        return UserInfoAllAllowedFields(**db_user.__dict__)

    return UserInfo(**db_user.__dict__)


@router.put(
    "/{user_id}",
    response_model=Union[UserInfoAllAllowedFields, UserInfo],
)
def update_user(
    user_id: int,
    req_user: UserUpdateAllAllowedFields,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Update an User stored in the database
    """
    current_user = auth.get_authenteficated_user(db, Auth)
    if not current_user.is_admin:
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        if isinstance(req_user.is_active, bool) or isinstance(req_user.is_admin, bool):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Update status not allowed",
            )

        req_user = UserUpdate(**req_user.__dict__)
    elif req_user.is_admin == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Update status not allowed",
        )

    updated_user = user.update(db, user_id, req_user)
    if current_user.is_admin:
        return UserInfoAllAllowedFields(**updated_user.__dict__)

    return UserInfo(**updated_user.__dict__)


@router.delete("/{user_id}", response_model=StatusResponse)
def delete_user(
    user_id: int,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Delete the User with the given ID
    """
    auth.is_only_admin_permitted(db, Auth)
    user.delete(db, user_id)

    return {"success": True, "message": "User deleted successfully"}
