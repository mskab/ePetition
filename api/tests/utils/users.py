import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.db.models.user import User
from api.db.repository.user import create, get_by_email
from api.core.hashing import Hasher
from api.schemas.user import UserCreate

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from utils.constants import ADMIN_TEST_DATA, USER_TEST_DATA
from utils.requests import user_login


def user_authentication_headers(client: TestClient, email: str, password: str):
    """
    Form access header for requests
    """
    response =  user_login(client, email, password).json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    user = get_by_email(db, email)
    if not user:
        user_in_create = UserCreate(
                            firstname=USER_TEST_DATA["firstname"],
                            lastname=USER_TEST_DATA["lastname"],
                            email=USER_TEST_DATA["email"],
                            password=USER_TEST_DATA["password"]
                        )
        user = create(user=user_in_create, _db=db)
    return user_authentication_headers(client=client, email=email, password=USER_TEST_DATA["password"])


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


def update_user_date_with_given_number(users_number, user=USER_TEST_DATA):
        return dict([(key, f"{users_number}{value}") for key, value in user.items()])
