from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.user import UserCreate, UserInfo, UserUpdate
from db.session import get_db
from db.repository import user

router = APIRouter()


@router.post("/", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create an User and store it in the database
    """
    return user.create(db, user)


@router.get('/', response_model=List[UserInfo])
def get_all_users(db: Session = Depends(get_db)):
    """
    Get all the Users stored in database
    """
    return user.get_all(db)


@router.get('/{user_id}', response_model=UserInfo)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get the User with the given ID
    """
    return user.get_by_id(db, user_id)


@router.put('/{user_id}', response_model=UserInfo)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an User stored in the database
    """
    return user.update(db, user_id, user)


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete the User with the given ID
    """
    user.delete(db, user_id)

    return "User deleted successfully"
