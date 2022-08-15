import json
from datetime import datetime
from utils.constants import DECISION_MAKER_TEST_DATA, PETITION_TEST_DATA, COMPLAINT_TEST_DATA


def test_create_complaint(client, normal_user_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    response_dm = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert response_dm.status_code == 201
    response_dm_json = response_dm.json()

    response_petition = client.post("/petitions/", data=json.dumps(dict(PETITION_TEST_DATA, **{"owner_id": 1, "decision_makers": [1]})), headers=normal_user_token_headers)
    assert 201 == response_petition.status_code
    response_petition_json = response_petition.json()
    assert response_petition_json.pop("decision_makers")[0] == response_dm_json
    assert dict(PETITION_TEST_DATA, **{"id": 1, "image": None, "owner_id": 1, "status": "pending", "supporters": [], "creation_date": str(datetime.now().date())}) == response_petition_json

    passed_complaint = dict(COMPLAINT_TEST_DATA, **{"owner_id": 1, "petition_id": 1})
    response_complaint = client.post("/complaints/", data=json.dumps(passed_complaint), headers=normal_user_token_headers)
    assert 201 == response_complaint.status_code
    assert dict(passed_complaint, **{"id": 1, "status": "pending"}) == response_complaint.json()


def test_get_all_complaint(client, normal_user_token_headers, primary_admin_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    primary_admin_token_headers.update({"Content-Type": "application/json"})
    response_dm = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert response_dm.status_code == 201
    response_dm_json = response_dm.json()

    response_petition = client.post("/petitions/", data=json.dumps(dict(PETITION_TEST_DATA, **{"owner_id": 1, "decision_makers": [1]})), headers=normal_user_token_headers)
    assert 201 == response_petition.status_code
    response_petition_json = response_petition.json()
    assert response_petition_json.pop("decision_makers")[0] == response_dm_json
    assert dict(PETITION_TEST_DATA, **{"id": 1, "image": None, "owner_id": 1, "status": "pending", "supporters": [], "creation_date": str(datetime.now().date())}) == response_petition_json

    passed_complaint = dict(COMPLAINT_TEST_DATA, **{"owner_id": 1, "petition_id": 1})
    response_complaint = client.post("/complaints/", data=json.dumps(passed_complaint), headers=normal_user_token_headers)
    assert 201 == response_complaint.status_code
    assert dict(passed_complaint, **{"id": 1, "status": "pending"}) == response_complaint.json()

    response_complaint = client.get("/complaints/", headers=primary_admin_token_headers)
    assert 200 == response_complaint.status_code
    assert 1 == len(response_complaint.json())
    assert dict(passed_complaint, **{"id": 1, "status": "pending"}) == response_complaint.json()[0]

def test_get_by_id_complaint(client, normal_user_token_headers, primary_admin_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    primary_admin_token_headers.update({"Content-Type": "application/json"})
    response_dm = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert response_dm.status_code == 201
    response_dm_json = response_dm.json()

    response_petition = client.post("/petitions/", data=json.dumps(dict(PETITION_TEST_DATA, **{"owner_id": 1, "decision_makers": [1]})), headers=normal_user_token_headers)
    assert 201 == response_petition.status_code
    response_petition_json = response_petition.json()
    assert response_petition_json.pop("decision_makers")[0] == response_dm_json
    assert dict(PETITION_TEST_DATA, **{"id": 1, "image": None, "owner_id": 1, "status": "pending", "supporters": [], "creation_date": str(datetime.now().date())}) == response_petition_json

    passed_complaint = dict(COMPLAINT_TEST_DATA, **{"owner_id": 1, "petition_id": 1})
    response_complaint = client.post("/complaints/", data=json.dumps(passed_complaint), headers=normal_user_token_headers)
    assert 201 == response_complaint.status_code
    assert dict(passed_complaint, **{"id": 1, "status": "pending"}) == response_complaint.json()

    response_complaint = client.get(f"/complaints/{1}", headers=primary_admin_token_headers)
    assert 200 == response_complaint.status_code
    assert dict(passed_complaint, **{"id": 1, "status": "pending"}) == response_complaint.json()


def test_delete_complaint_by_id(client, normal_user_token_headers, primary_admin_token_headers):
    normal_user_token_headers.update({"Content-Type": "application/json"})
    primary_admin_token_headers.update({"Content-Type": "application/json"})
    response_dm = client.post("/decision_makers/", data=json.dumps(DECISION_MAKER_TEST_DATA), headers=normal_user_token_headers)
    assert response_dm.status_code == 201
    response_dm_json = response_dm.json()

    response_petition = client.post("/petitions/", data=json.dumps(dict(PETITION_TEST_DATA, **{"owner_id": 1, "decision_makers": [1]})), headers=normal_user_token_headers)
    assert 201 == response_petition.status_code
    response_petition_json = response_petition.json()
    assert response_petition_json.pop("decision_makers")[0] == response_dm_json
    assert dict(PETITION_TEST_DATA, **{"id": 1, "image": None, "owner_id": 1, "status": "pending", "supporters": [], "creation_date": str(datetime.now().date())}) == response_petition_json

    passed_complaint = dict(COMPLAINT_TEST_DATA, **{"owner_id": 1, "petition_id": 1})
    response_complaint = client.post("/complaints/", data=json.dumps(passed_complaint), headers=normal_user_token_headers)
    assert 201 == response_complaint.status_code
    assert dict(passed_complaint, **{"id": 1, "status": "pending"}) == response_complaint.json()

    response_complaint = client.delete(f"/complaints/{1}", headers=primary_admin_token_headers)
    assert 200 == response_complaint.status_code
    assert "Complaint deleted successfully" == response_complaint.json()["message"]

    response_complaint = client.get(f"/complaints/{1}", headers=primary_admin_token_headers)
    assert 404 == response_complaint.status_code
