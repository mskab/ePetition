import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.models.user import User
from db.repository.user import create, get_by_email
from core.hashing import Hasher
from schemas.user import UserCreate

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from utils.constants import ADMIN_TEST_DATA


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    response = client.post("/auth/login", data=data).json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    user = get_by_email(email=email, db=db)
    if not user:
        user_in_create = UserCreate(
                            firstname="firstname",
                            lastname="lastname",
                            email=email,
                            password=Hasher.get_password_hash(password)
                        )
        user = create(user=user_in_create, db=db)
    return user_authentication_headers(client=client, email=email, password=password)


def register_admin_to_db(client: TestClient, db: Session):
    db_user = User(
        firstname=ADMIN_TEST_DATA["firstname"],
        lastname=ADMIN_TEST_DATA["lastname"],
        email=ADMIN_TEST_DATA["email"],
        password=Hasher.get_password_hash(ADMIN_TEST_DATA["password"]),
        is_admin=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return user_authentication_headers(client=client, email=ADMIN_TEST_DATA["email"], password=ADMIN_TEST_DATA["password"])
