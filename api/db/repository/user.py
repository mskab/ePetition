from api.core.hashing import Hasher
from api.db.models.user import User
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from api.schemas.user import UserCreate, UserUpdateAllAllowedFields
from sqlalchemy import or_
from sqlalchemy.orm import Session


def create(_db: Session, user: UserCreate):
    is_user_exist_by_email(_db, user.email)
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=Hasher.get_password_hash(user.password),
    )
    _db.add(db_user)
    _db.commit()
    _db.refresh(db_user)

    return db_user


def get_by_email(_db: Session, email: str):
    return _db.query(User).filter(User.email == email).first()


def is_user_exist_by_email(_db: Session, email: str):
    db_user = get_by_email(_db, email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )


def get_by_id(_db: Session, user_id: int):
    db_user = _db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with the given ID",
        )

    return db_user


def get_all(
    _db: Session,
    offset: int = 0,
    limit: int = 100,
    search_query: str = "",
    is_active: bool = None,
    is_admin: bool = None,
):
    query = _db.query(User).filter(
        or_(
            User.firstname.contains(search_query, autoescape=True),
            User.lastname.contains(search_query, autoescape=True),
            User.email.contains(search_query, autoescape=True),
        )
    )
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)

    return query.offset(offset).limit(limit).all()


def update(
    _db: Session, user_id: int, user: UserUpdateAllAllowedFields
):
    db_user = get_by_id(_db, user_id)
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

    if update_user_encoded.get("is_active") is not None:
        db_user.is_active = update_user_encoded["is_active"]

    if update_user_encoded.get("is_admin"):
        db_user.is_admin = update_user_encoded["is_admin"]

    _db.commit()
    _db.refresh(db_user)

    return db_user


def delete(_db: Session, user_id: int):
    user = get_by_id(_db, user_id)
    _db.delete(user)
    _db.commit()
