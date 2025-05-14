def test_create_user(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "89998887777",
        "password": "testpass",
        "department_id": None,
        "status": "ACTIVE",
    }

    response = client.post(
        "/api/v1/users",
        json=user_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert "id" in response.json


def test_get_user(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "+12345678901",
        "password": "testpass",
        "department_id": None
    }
    create_response = client.post("/api/v1/users", json=user_data, query_string=auth_apikey)
    user_id = create_response.json["id"]

    response = client.get(f"/api/v1/users/{user_id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert response.json["users"]["name"] == "Test User"


def test_update_user(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "+12345678902",
        "password": "testpass",
        "department_id": None
    }
    create_response = client.post("/api/v1/users", json=user_data, query_string=auth_apikey)
    user_id = create_response.json["id"]

    update_data = {"name": "Updated Name"}
    response = client.put(
        f"/api/v1/users/{user_id}",
        json=update_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert response.json["success"] == "OK"


def test_delete_user(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "+12345678903",
        "password": "testpass",
        "department_id": None
    }
    create_response = client.post("/api/v1/users", json=user_data, query_string=auth_apikey)
    user_id = create_response.json["id"]

    response = client.delete(f"/api/v1/users/{user_id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert response.json["success"] == "OK"
