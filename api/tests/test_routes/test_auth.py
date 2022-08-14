import json
from utils.constants import USER_TEST_DATA, AUTH_ERRORS
from utils.requests import user_login


def test_auth(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    response_json = response.json()
    assert USER_TEST_DATA["email"] == response_json["email"]
    assert USER_TEST_DATA["firstname"] == response_json["firstname"]
    assert USER_TEST_DATA["lastname"] == response_json["lastname"]

    response = user_login(client)
    assert 200 == response.status_code
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data


def test_auth_error_password_not_mutch_email(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    response_json = response.json()
    assert USER_TEST_DATA["email"] == response_json["email"]
    assert USER_TEST_DATA["firstname"] == response_json["firstname"]
    assert USER_TEST_DATA["lastname"] == response_json["lastname"]

    response = user_login(client, password="wrong_password")
    assert response.status_code == 401
    assert AUTH_ERRORS["password_not_mutch_email"] == response.json()["detail"]


def test_auth_error_email_not_exist(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    response_json = response.json()
    assert USER_TEST_DATA["email"] == response_json["email"]
    assert USER_TEST_DATA["firstname"] == response_json["firstname"]
    assert USER_TEST_DATA["lastname"] == response_json["lastname"]

    response = user_login(client, username="email_not_exist@ene.com")
    assert 404 == response.status_code
    assert AUTH_ERRORS["email_not_exist"] == response.json()["detail"]


def test_auth_error_account_inactive(client, primary_admin_token_headers):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    response_json = response.json()
    assert response_json["email"] == USER_TEST_DATA["email"]
    assert response_json["firstname"] == USER_TEST_DATA["firstname"]
    assert response_json["lastname"] == USER_TEST_DATA["lastname"]

    admin_headers = primary_admin_token_headers
    admin_headers.update({"Content-Type": "application/json"})

    response =  client.put(f"users/{response_json['id']}",
                    headers=admin_headers,
                    data=json.dumps({"is_active": False}))
    assert 200 == response.status_code
    is_active = response.json()["is_active"]
    assert isinstance(is_active,bool) and not is_active

    response =  user_login(client)
    assert 409 == response.status_code
    assert AUTH_ERRORS["account_inactive"] == response.json()["detail"]


def test_refresh(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    response_json = response.json()
    assert USER_TEST_DATA["email"] == response_json["email"]
    assert USER_TEST_DATA["firstname"] == response_json["firstname"]
    assert USER_TEST_DATA["lastname"] == response_json["lastname"]

    response_login =user_login(client)
    assert response_login.status_code == 200
    response_login = response_login.json()
    assert "access_token" in response_login
    assert "refresh_token" in response_login

    refresh_token = f"Bearer {response_login['refresh_token']}"
    response_refresh = client.post("/auth/refresh", headers={"authorization": refresh_token})
    assert response_refresh.status_code == 200
    response_refresh = response_refresh.json()
    assert "access_token" in response_refresh
    assert "refresh_token" not in response_refresh
    assert response_login["access_token"] != response_refresh["access_token"]
