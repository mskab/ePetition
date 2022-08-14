import json
from utils.constants import USER_TEST_DATA

def test_auth(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    assert response.json()["email"] == USER_TEST_DATA["email"]
    assert response.json()["firstname"] == USER_TEST_DATA["firstname"]
    assert response.json()["lastname"] == USER_TEST_DATA["lastname"]

    response = client.post("/auth/login", data={"username": USER_TEST_DATA["email"], "password": USER_TEST_DATA["password"]})
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data

def test_refresh(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    assert response.json()["email"] == USER_TEST_DATA["email"]
    assert response.json()["firstname"] == USER_TEST_DATA["firstname"]
    assert response.json()["lastname"] == USER_TEST_DATA["lastname"]

    response_login = client.post("/auth/login", data={"username": USER_TEST_DATA["email"], "password": USER_TEST_DATA["password"]})
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
