import json
import asyncio
import pytest
from utils.constants import USER_TEST_DATA, ADMIN_TEST_DATA, USER_MESSAGES
from utils.common import remove_fields_from_dict, list_of_dict_to_set_of_fsets
from utils.requests import async_get_user_by_id, get_all_users
from utils.users import update_user_date_with_given_number


def test_create_user(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    assert response.status_code == 201
    response_json = response.json()
    assert USER_TEST_DATA["email"] == response_json["email"]
    assert USER_TEST_DATA["firstname"] == response_json["firstname"]
    assert USER_TEST_DATA["lastname"] == response_json["lastname"]


def test_error_create_user_already_exist(client):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    assert response.status_code == 201
    response_json = response.json()
    assert USER_TEST_DATA["email"] == response_json["email"]
    assert USER_TEST_DATA["firstname"] == response_json["firstname"]
    assert USER_TEST_DATA["lastname"] == response_json["lastname"]

    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    assert 409 == response.status_code
    assert USER_MESSAGES["user_already_exist"] == response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_users(client, primary_admin_token_headers):
    all_users_response = get_all_users(client, primary_admin_token_headers)
    assert 200 == all_users_response.status_code
    assert 1 == len(all_users_response.json())

    async def create_user(user_number):
        user = update_user_date_with_given_number(user_number)
        return client.post("/users/", json.dumps(user))

    tasks = [asyncio.create_task(create_user(user_number))
             for user_number in range(10)]
    results = await asyncio.gather(*tasks)

    expected_result = [(201, remove_fields_from_dict(update_user_date_with_given_number(
        user_number), ["password"])) for user_number in range(10)]
    obtained_result = []
    for result in results:
        obtained_result.append(
            (result.status_code, remove_fields_from_dict(result.json(), ["id"])))

    assert 10 == len(results)
    assert expected_result == obtained_result

    all_users_response = get_all_users(client, primary_admin_token_headers)

    obtained_result = [remove_fields_from_dict(
        user_, ["id"]) for user_ in all_users_response.json()]

    expected_result = [remove_fields_from_dict(update_user_date_with_given_number(
        user_number), ["password"]) for user_number in range(10)]
    expected_result = [dict(
        user_, **{"is_admin": False, "is_active": True}) for user_ in expected_result]

    test_admin = ADMIN_TEST_DATA.copy()
    expected_result.append(dict(remove_fields_from_dict(
        test_admin, ["password"]), **{"is_admin": True, 'is_active': True}))

    assert 200 == all_users_response.status_code
    assert 11 == len(obtained_result)
    assert list_of_dict_to_set_of_fsets(expected_result) == list_of_dict_to_set_of_fsets(obtained_result)


@pytest.mark.asyncio
async def test_admin_get_user_by_id(client, normal_user_token_headers, primary_admin_token_headers):
    all_users_response = get_all_users(client, primary_admin_token_headers)

    all_users_response_json = all_users_response.json()
    assert 200 == all_users_response.status_code
    assert 2 == len(all_users_response_json)

    tasks = [asyncio.create_task(async_get_user_by_id(client, user_['id'], primary_admin_token_headers))
             for user_ in all_users_response_json]
    results = await asyncio.gather(*tasks)

    for result in results:
        assert 200 == result.status_code
    results_json = [result.json() for result in results]
    assert 2 == len(results_json)
    assert list_of_dict_to_set_of_fsets(all_users_response_json) == list_of_dict_to_set_of_fsets(results_json)


@pytest.mark.asyncio
async def test_user_get_user_by_id(client, normal_user_token_headers, primary_admin_token_headers):
    all_users_response = get_all_users(client, primary_admin_token_headers)

    all_users_response_json = all_users_response.json()
    assert 200 == all_users_response.status_code
    assert 2 == len(all_users_response_json)

    tasks = [asyncio.create_task(async_get_user_by_id(client, user_['id'], normal_user_token_headers))
             for user_ in all_users_response_json]
    results = await asyncio.gather(*tasks)

    for result in results:
        if result.status_code == 200:
            assert result.json()["email"] == USER_TEST_DATA["email"]
        else:
            assert "Forbidden" == result.json()["detail"]
    results_json = [result.json() for result in results]
    assert 2 == len(results_json)
    assert list_of_dict_to_set_of_fsets(all_users_response_json) != list_of_dict_to_set_of_fsets(results_json)


@pytest.mark.asyncio
async def test_user_put(client, normal_user_token_headers, primary_admin_token_headers):
    async def user_update(user_id, user_, headers_):
        return client.put(f"/users/{user_id}",
                            headers=headers_,
                            data=json.dumps(remove_fields_from_dict(user_, ["id"])))

    all_users_response = get_all_users(client, primary_admin_token_headers)

    all_users_response_json = all_users_response.json()
    assert 200 == all_users_response.status_code
    assert 2 == len(all_users_response_json)

    admin_headers = primary_admin_token_headers
    admin_headers.update({"Content-Type": "application/json"})

    all_users_response_json = [remove_fields_from_dict(user_.copy(), ["is_active", "is_admin"]) for user_ in all_users_response_json]

    tasks = [asyncio.create_task(user_update(user_['id'], update_user_date_with_given_number(user_['id'], user_), admin_headers))
             for user_ in all_users_response_json]

    results = await asyncio.gather(*tasks)

    tasks = []
    for result in results:
        assert 200 == result.status_code
        result_json =result.json()
        if result_json["email"] == f"{result_json['id']}{USER_TEST_DATA['email']}":
            expected_updated_user = update_user_date_with_given_number(result_json["id"], USER_TEST_DATA)
        else:
            expected_updated_user = update_user_date_with_given_number(result_json["id"], ADMIN_TEST_DATA)

        assert remove_fields_from_dict(expected_updated_user, ["password"]) == remove_fields_from_dict(result_json.copy(), ["is_active", "is_admin", "id"])


def test_user_delete(client, primary_admin_token_headers):
    response = client.post("/users/", json.dumps(USER_TEST_DATA))
    assert response.status_code == 201
    response_json = response.json()
    assert USER_TEST_DATA["email"] == response_json["email"]
    assert USER_TEST_DATA["firstname"] == response_json["firstname"]
    assert USER_TEST_DATA["lastname"] == response_json["lastname"]

    response = client.delete(f"/users/{response_json['id']}", headers=primary_admin_token_headers)

    assert 200 == response.status_code
    assert USER_MESSAGES["user_deleted"] == response.json()["message"]

    response = client.get(f"/users/{response_json['id']}", headers=primary_admin_token_headers)
    assert 404 == response.status_code
    assert USER_MESSAGES["user_not_found_with_id"] == response.json()["detail"]
