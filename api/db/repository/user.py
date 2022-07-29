from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserBase
from db.models.user import User
from core.hashing import Hasher
from fastapi.encoders import jsonable_encoder


async def create(db: Session, user: UserCreate):
    db_user = User(firstname=user.firstname,
                   lastname=user.lastname,
                   email=user.email,
                   password=Hasher.get_password_hash(user.password),
                   is_active=True,
                   is_admin=False
                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update(db: Session, user_id: int, user: UserBase):
    db_user = get_by_id(db, user_id)
    if db_user:
        update_user_encoded = jsonable_encoder(user)
        if update_user_encoded['firstname']:
            db_user.firstname = update_user_encoded['firstname']
        if update_user_encoded['lastname']:
            db_user.lastname = update_user_encoded['lastname']
        if update_user_encoded['email']:
            db_user.email = update_user_encoded['email']
        if update_user_encoded['password']:
            db_user.password = Hasher.get_password_hash(
                update_user_encoded['password'])
        db.commit()
        db.refresh(db_user)
    return db_user


def delete(db: Session, user_id: int):
    user = get_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()

    return user
