import json
import asyncio
import pytest
from utils.constants import USER_TEST_DATA, ADMIN_TEST_DATA
from utils.common import remove_fields_from_dict

def test_create_user(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    assert response.status_code == 201
    assert response.json()["email"] == USER_TEST_DATA["email"]
    assert response.json()["firstname"] == USER_TEST_DATA["firstname"]
    assert response.json()["lastname"] == USER_TEST_DATA["lastname"]


@pytest.mark.asyncio
async def test_get_all_users(client, primary_admin_token_headers):
    def generate_user_data(user_number):
        return dict([(key, f"{user_number}{value}") for key, value in USER_TEST_DATA.items()])

    async def create_user(user_number):
        user = generate_user_data(user_number)
        return client.post("/users/", json.dumps(user))

    tasks = [asyncio.create_task(create_user(user_number)) for user_number in range(10)]
    results = await asyncio.gather(*tasks)

    expected_result = [(201, remove_fields_from_dict(generate_user_data(user_number), ["password"])) for user_number in range(10)]
    obtained_result = []
    for result in results:
        obtained_result.append((result.status_code, remove_fields_from_dict(result.json(), ["id"])))

    assert 10 == len(results)
    assert expected_result == obtained_result

    all_users_response = client.get("/users/", headers=primary_admin_token_headers)

    obtained_result = [remove_fields_from_dict(user_, ["id"]) for user_ in all_users_response.json()]

    expected_result = [remove_fields_from_dict(generate_user_data(user_number), ["password"]) for user_number in range(10)]
    expected_result = [dict(user_, **{"is_admin": False, "is_active": True}) for user_ in expected_result]
    expected_result.append(dict(remove_fields_from_dict(ADMIN_TEST_DATA, ["password"]), **{"is_admin": True, 'is_active': True}))

    assert 200 == all_users_response.status_code
    assert 11 == len(obtained_result)
    assert set(frozenset(d.items()) for d in expected_result) == set(frozenset(d.items()) for d in obtained_result)
