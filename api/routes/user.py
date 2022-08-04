from typing import List

from db.repository import user
from db.session import get_db
from fastapi import APIRouter, Depends, status
from schemas.user import UserCreate, UserInfo, UserUpdate
from sqlalchemy.orm import Session

router = APIRouter()
default_session = Depends(get_db)


@router.post(
    "/", response_model=UserInfo, status_code=status.HTTP_201_CREATED
)
def create_user(req_user: UserCreate, db: Session = default_session):
    """
    Create an User and store it in the database
    """
    return user.create(db, req_user)


@router.get("/", response_model=List[UserInfo])
def get_all_users(
    offset: int, limit: int, db: Session = default_session
):
    """
    Get all the Users stored in database
    """
    return user.get_all(db, offset, limit)


@router.get("/{user_id}", response_model=UserInfo)
def get_user(user_id: int, db: Session = default_session):
    """
    Get the User with the given ID
    """
    return user.get_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserInfo)
def update_user(
    user_id: int, req_user: UserUpdate, db: Session = default_session
):
    """
    Update an User stored in the database
    """
    return user.update(db, user_id, req_user)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = default_session):
    """
    Delete the User with the given ID
    """
    user.delete(db, user_id)

    return "User deleted successfully"
