from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from db.models.user import User
from core.hashing import Hasher
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


def create(db: Session, user: UserCreate):
    is_user_exist_by_email(db, user.email)
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=Hasher.get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def is_user_exist_by_email(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )


def get_by_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with the given ID",
        )

    return db_user


def get_all(db: Session, offset: int = 0, limit: int = 100):
    return db.query(User).offset(offset).limit(limit).all()


def update(db: Session, user_id: int, user: UserUpdate):
    db_user = get_by_id(db, user_id)
    update_user_encoded = jsonable_encoder(user)
    if update_user_encoded["firstname"]:
        db_user.firstname = update_user_encoded["firstname"]

    if update_user_encoded["lastname"]:
        db_user.lastname = update_user_encoded["lastname"]

    if update_user_encoded["email"]:
        db_user.email = update_user_encoded["email"]

    if update_user_encoded["password"]:
        db_user.password = Hasher.get_password_hash(
            update_user_encoded["password"]
        )

    db.commit()
    db.refresh(db_user)

    return db_user


def delete(db: Session, user_id: int):
    user = get_by_id(db, user_id)
    db.delete(user)
    db.commit()
