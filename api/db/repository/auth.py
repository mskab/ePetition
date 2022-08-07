from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from core.hashing import Hasher
from db.repository import user


def authenticate_user(_db: Session, email: str, password: str):
    db_user = user.get_by_email(_db, email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email does not exist",
        )
    if not Hasher.verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password does not match the email provided",
        )
    return db_user
