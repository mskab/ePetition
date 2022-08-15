import json
import asyncio
import pytest
from utils.constants import DECISION_MAKER_TEST_DATA, DECISION_MAKER_MESSAGES
from utils.common import list_of_dict_to_set_of_fsets, remove_fields_from_dict


def test_create_decision_maker(client, normal_user_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    response = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert 201 == response.status_code
    response_json = response.json()
    assert DECISION_MAKER_TEST_DATA["email"] == response_json["email"]
    assert DECISION_MAKER_TEST_DATA["naming"] == response_json["naming"]
    assert DECISION_MAKER_TEST_DATA["affiliation"] == response_json["affiliation"]


def test_error_such_decision_maker_already_exists_create_petition_user(client, normal_user_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    response = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert 201 == response.status_code
    response_json = response.json()
    assert DECISION_MAKER_TEST_DATA["email"] == response_json["email"]
    assert DECISION_MAKER_TEST_DATA["naming"] == response_json["naming"]
    assert DECISION_MAKER_TEST_DATA["affiliation"] == response_json["affiliation"]

    response = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert 409 == response.status_code
    assert DECISION_MAKER_MESSAGES["already_exist"] == response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_decision_makers(client, normal_user_token_headers):
    def generate_decision_maker(number):
        return dict([(key, f"{number}{value}") for key, value in DECISION_MAKER_TEST_DATA.items()])
    async def create_decision_maker(number):
        decision_maker = generate_decision_maker(number)
        return client.post("/decision_makers/", data=json.dumps(decision_maker), headers=normal_user_token_headers)

    tasks = [asyncio.create_task(create_decision_maker(number))
             for number in range(100)]
    results = await asyncio.gather(*tasks)

    assert any([result.status_code == 201 for result in results])
    results_json = [remove_fields_from_dict(result.json(), ["id", "is_verified"]) for result in results]

    expected_decision_makers = [generate_decision_maker(number) for number in range(100)]
    assert list_of_dict_to_set_of_fsets(expected_decision_makers) == list_of_dict_to_set_of_fsets(results_json)

    decision_makers = client.get("/decision_makers/")
    expected_decision_makers = [dict(generate_decision_maker(number), **{"id": number + 1, "is_verified": False}) for number in range(100)]

    assert list_of_dict_to_set_of_fsets(decision_makers.json()) == list_of_dict_to_set_of_fsets(expected_decision_makers)


@pytest.mark.asyncio
async def test_get_decision_maker_by_id(client, normal_user_token_headers):
    def generate_decision_maker(number):
        return dict([(key, f"{number}{value}") for key, value in DECISION_MAKER_TEST_DATA.items()])
    async def create_decision_maker(number):
        decision_maker = generate_decision_maker(number)
        return client.post("/decision_makers/", data=json.dumps(decision_maker), headers=normal_user_token_headers)

    async def get_by_id_decision_maker(id):
        return client.get(f"/decision_makers/{id}")

    tasks = [asyncio.create_task(create_decision_maker(number))
             for number in range(100)]
    results = await asyncio.gather(*tasks)

    assert any([result.status_code == 201 for result in results])
    results_json = [remove_fields_from_dict(result.json(), ["id", "is_verified"]) for result in results]

    expected_decision_makers = [generate_decision_maker(number) for number in range(100)]
    assert list_of_dict_to_set_of_fsets(expected_decision_makers) == list_of_dict_to_set_of_fsets(results_json)

    tasks = [asyncio.create_task(get_by_id_decision_maker(number))
             for number in range(1, 101)]
    results = await asyncio.gather(*tasks)
    assert any([result.status_code == 200 for result in results])
    results_json = [result.json() for result in results]
    expected_decision_makers = [dict(generate_decision_maker(number), **{"id": number + 1, "is_verified": False}) for number in range(100)]
    assert list_of_dict_to_set_of_fsets(results_json) == list_of_dict_to_set_of_fsets(expected_decision_makers)


def test_update_decision_maker(client, normal_user_token_headers, primary_admin_token_headers):
    response = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    dm_copy = DECISION_MAKER_TEST_DATA.copy()
    assert 201 == response.status_code
    assert dict(dm_copy, **{"id": 1, "is_verified": False}) == response.json()

    response = client.put(f"/decision_makers/{1}", data=json.dumps({"is_verified": True}), headers=normal_user_token_headers)
    assert 403 == response.status_code

    response = client.put(f"/decision_makers/{1}", data=json.dumps({"is_verified": True}), headers=primary_admin_token_headers)
    assert 200 == response.status_code
    assert dict(DECISION_MAKER_TEST_DATA, **{"id": 1, "is_verified": True}) == response.json()


def test_delete_decision_maker(client, normal_user_token_headers, primary_admin_token_headers):
    response = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)

    assert 201 == response.status_code
    assert dict(DECISION_MAKER_TEST_DATA, **{"id": 1, "is_verified": False}) == response.json()

    response = client.delete(f"/decision_makers/{1}", headers=normal_user_token_headers)
    assert 403 == response.status_code

    response = client.delete(f"/decision_makers/{1}", headers=primary_admin_token_headers)
    assert 200 == response.status_code
    assert DECISION_MAKER_MESSAGES["deleted"] == response.json()["message"]

    response = client.get(f"/decision_makers/{1}", headers=primary_admin_token_headers)
    assert 404 == response.status_code
    assert DECISION_MAKER_MESSAGES["not_found"] == response.json()["detail"]
