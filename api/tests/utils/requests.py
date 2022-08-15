from utils.constants import USER_TEST_DATA


async def async_get_user_by_id(client, id, headers):
    return client.get(f"/users/{id}", headers=headers)


def user_login(client, username=USER_TEST_DATA["email"], password=USER_TEST_DATA["password"]):
    return client.post("/auth/login", data={"username": username, "password": password})


def get_all_users(client, headers):
    return client.get("/users/", headers=headers)
