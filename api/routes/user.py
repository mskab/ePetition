from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.user import UserCreate, UserInfo, UserBase
from db.session import get_db
from db.repository import user as repo

router = APIRouter()


@router.post("/", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create an User and store it in the database
    """
    db_user = repo.get_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return await repo.create(db, user)


@router.get('/', response_model=List[UserInfo])
def get_all_users(db: Session = Depends(get_db)):
    """
    Get all the Users stored in database
    """
    return repo.get_all(db)


@router.get('/{user_id}', response_model=UserInfo)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get the User with the given ID
    """
    user = repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found with the given ID")

    return user


@router.put('/{user_id}', response_model=UserInfo)
def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    """
    Update an User stored in the database
    """
    user = repo.update(db, user_id, user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found with the given ID")
    return user


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete the User with the given ID
    """
    user = repo.delete(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found with the given ID")

    return "User deleted successfully"
