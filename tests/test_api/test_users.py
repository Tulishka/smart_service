from app.users.models import User
from tests.test_api.conftest import API_PREFIX


def test_create_user(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "89998887777",
        "password": "testpass",
        "department_id": None,
        "status": "ACTIVE",
    }

    response = client.post(
        f"{API_PREFIX}/users",
        json=user_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert "id" in response.json


def test_get_user(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "89998887778",
        "password": "testpass",
        "department_id": None
    }
    create_response = client.post(f"{API_PREFIX}/users", json=user_data, query_string=auth_apikey)
    user_id = create_response.json["id"]

    response = client.get(f"{API_PREFIX}/users/{user_id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert response.json["users"]["name"] == "Test User"


def test_update_user(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "89998887779",
        "password": "testpass",
        "department_id": None
    }
    create_response = client.post(f"{API_PREFIX}/users", json=user_data, query_string=auth_apikey)
    user_id = create_response.json["id"]

    update_data = {"name": "Updated Name"}
    response = client.put(
        f"{API_PREFIX}/users/{user_id}",
        json=update_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert response.json["success"] == "OK"


def test_delete_user(client, auth_apikey, db):
    user_data = {
        "name": "Test User",
        "phone": "89998887710",
        "password": "testpass",
        "department_id": None
    }
    create_response = client.post(f"{API_PREFIX}/users", json=user_data, query_string=auth_apikey)
    user_id = create_response.json["id"]

    response = client.delete(f"{API_PREFIX}/users/{user_id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert response.json["success"] == "OK"
    assert User.query.filter_by(id=user_id).one_or_none() is None
