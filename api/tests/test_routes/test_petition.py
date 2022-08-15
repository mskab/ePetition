import json
from datetime import datetime
from utils.constants import DECISION_MAKER_TEST_DATA, PETITION_TEST_DATA
from utils.common import list_of_dict_to_set_of_fsets, remove_fields_from_dict


def test_create_petition(client, normal_user_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    response_dm = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert response_dm.status_code == 201
    response_dm_json = response_dm.json()

    response_petition = client.post("/petitions/", data=json.dumps(dict(PETITION_TEST_DATA, **{"owner_id": 1, "decision_makers": [1]})), headers=normal_user_token_headers)
    assert 201 == response_petition.status_code
    response_petition_json = response_petition.json()
    assert response_petition_json.pop("decision_makers")[0] == response_dm_json
    assert dict(PETITION_TEST_DATA, **{"id": 1, "image": None, "owner_id": 1, "status": "pending", "supporters": [], "creation_date": str(datetime.now().date())}) == response_petition_json


def test_get_all_petitions(client, normal_user_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    response_dm = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert response_dm.status_code == 201
    response_dm_json = response_dm.json()

    created_petition = client.post("/petitions/", data=json.dumps(dict(PETITION_TEST_DATA, **{"owner_id": 1, "decision_makers": [1], 'due_date': '2001-01-01'})), headers=normal_user_token_headers)

    assert created_petition.status_code == 201
    assert created_petition.json().pop("decision_makers")[0] == response_dm_json
    assert created_petition.json().pop("supporters") == []
    results = remove_fields_from_dict(created_petition.json(), ["decision_makers", "id", "supporters"])
    expected_petitions = dict(PETITION_TEST_DATA, **{"image": None, "owner_id": 1, "status": "pending", "creation_date": str(datetime.now().date()), "due_date": '2001-01-01'})
    assert list_of_dict_to_set_of_fsets([expected_petitions]) == list_of_dict_to_set_of_fsets([results])

    result_petitions = client.get("/petitions/")
    assert result_petitions.status_code == 200
    result_petitions_json = remove_fields_from_dict(result_petitions.json()[0], ["decision_makers", "id", "supporters"])
    assert list_of_dict_to_set_of_fsets([expected_petitions]) == list_of_dict_to_set_of_fsets([result_petitions_json])


def test_get_petition_by_id(client, normal_user_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    response_dm = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert response_dm.status_code == 201
    response_dm_json = response_dm.json()

    created_petition = client.post("/petitions/", data=json.dumps(dict(PETITION_TEST_DATA, **{"owner_id": 1, "decision_makers": [1], 'due_date': '2001-01-01'})), headers=normal_user_token_headers)

    assert created_petition.status_code == 201
    assert created_petition.json().pop("decision_makers")[0] == response_dm_json
    assert created_petition.json().pop("supporters") == []
    results = remove_fields_from_dict(created_petition.json(), ["decision_makers", "id", "supporters"])
    expected_petitions = dict(PETITION_TEST_DATA, **{"image": None, "owner_id": 1, "status": "pending", "creation_date": str(datetime.now().date()), "due_date": '2001-01-01'})
    assert list_of_dict_to_set_of_fsets([expected_petitions]) == list_of_dict_to_set_of_fsets([results])

    result_petitions = client.get(f"/petitions/{1}")
    assert result_petitions.status_code == 200
    result_petitions_json = remove_fields_from_dict(result_petitions.json(), ["decision_makers", "id", "supporters"])
    assert list_of_dict_to_set_of_fsets([expected_petitions]) == list_of_dict_to_set_of_fsets([result_petitions_json])


def test_delete_petition_by_id(client, normal_user_token_headers, primary_admin_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    response_dm = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert response_dm.status_code == 201
    response_dm_json = response_dm.json()

    created_petition = client.post("/petitions/", data=json.dumps(dict(PETITION_TEST_DATA, **{"owner_id": 1, "decision_makers": [1], 'due_date': '2001-01-01'})), headers=normal_user_token_headers)

    assert created_petition.status_code == 201
    assert created_petition.json().pop("decision_makers")[0] == response_dm_json
    assert created_petition.json().pop("supporters") == []
    results = remove_fields_from_dict(created_petition.json(), ["decision_makers", "id", "supporters"])
    expected_petitions = dict(PETITION_TEST_DATA, **{"image": None, "owner_id": 1, "status": "pending", "creation_date": str(datetime.now().date()), "due_date": '2001-01-01'})
    assert list_of_dict_to_set_of_fsets([expected_petitions]) == list_of_dict_to_set_of_fsets([results])

    result_petitions = client.get(f"/petitions/{1}")
    assert result_petitions.status_code == 200
    result_petitions_json = remove_fields_from_dict(result_petitions.json(), ["decision_makers", "id", "supporters"])
    assert list_of_dict_to_set_of_fsets([expected_petitions]) == list_of_dict_to_set_of_fsets([result_petitions_json])

    result_petitions = client.delete(f"/petitions/{1}", headers=primary_admin_token_headers)
    assert result_petitions.status_code == 200
    assert "Petition deleted successfully" == result_petitions.json()["message"]

    result_petitions = client.get(f"/petitions/{1}", headers=primary_admin_token_headers)
    assert result_petitions.status_code == 404
