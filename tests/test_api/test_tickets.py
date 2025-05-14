def test_create_ticket(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "+12345678904",
        "password": "testpass",
        "department_id": None
    }
    user_response = client.post("/api/v1/users", json=user_data, query_string=auth_apikey)
    user_id = user_response.json["id"]

    asset_data = {
        "name": "Test Asset",
        "type_id": 1,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174004",
        "status": "ДОСТУПНО"
    }
    asset_response = client.post("/api/v1/assets", json=asset_data, query_string=auth_apikey)
    asset_id = asset_response.json["id"]

    ticket_data = {
        "asset_id": asset_id,
        "description": "Test description",
        "creator_id": user_id,
        "status": "ОТКРЫТ"
    }

    response = client.post(
        "/api/v1/tickets",
        json=ticket_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert "id" in response.json


def test_get_ticket(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "+12345678905",
        "password": "testpass",
        "department_id": None
    }
    user_response = client.post("/api/v1/users", json=user_data, query_string=auth_apikey)
    user_id = user_response.json["id"]

    asset_data = {
        "name": "Test Asset",
        "type_id": 1,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174005",
        "status": "ДОСТУПНО"
    }
    asset_response = client.post("/api/v1/assets", json=asset_data, query_string=auth_apikey)
    asset_id = asset_response.json["id"]

    ticket_data = {
        "asset_id": asset_id,
        "description": "Test description",
        "creator_id": user_id,
        "status": "ОТКРЫТ"
    }
    create_response = client.post("/api/v1/tickets", json=ticket_data, query_string=auth_apikey)
    ticket_id = create_response.json["id"]

    response = client.get(f"/api/v1/tickets/{ticket_id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert response.json["description"] == "Test description"


def test_update_ticket(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "+12345678906",
        "password": "testpass",
        "department_id": None
    }
    user_response = client.post("/api/v1/users", json=user_data, query_string=auth_apikey)
    user_id = user_response.json["id"]

    asset_data = {
        "name": "Test Asset",
        "type_id": 1,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174006",
        "status": "ДОСТУПНО"
    }
    asset_response = client.post("/api/v1/assets", json=asset_data, query_string=auth_apikey)
    asset_id = asset_response.json["id"]

    ticket_data = {
        "asset_id": asset_id,
        "description": "Test description",
        "creator_id": user_id,
        "status": "ОТКРЫТ"
    }
    create_response = client.post("/api/v1/tickets", json=ticket_data, query_string=auth_apikey)
    ticket_id = create_response.json["id"]

    update_data = {"status": "ЗАКРЫТ"}
    response = client.put(
        f"/api/v1/tickets/{ticket_id}",
        json=update_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert response.json["status"] == "ЗАКРЫТ"


def test_delete_ticket(client, auth_apikey):
    user_data = {
        "name": "Test User",
        "phone": "+12345678907",
        "password": "testpass",
        "department_id": None
    }
    user_response = client.post("/api/v1/users", json=user_data, query_string=auth_apikey)
    user_id = user_response.json["id"]

    asset_data = {
        "name": "Test Asset",
        "type_id": 1,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174007",
        "status": "ДОСТУПНО"
    }
    asset_response = client.post("/api/v1/assets", json=asset_data, query_string=auth_apikey)
    asset_id = asset_response.json["id"]

    ticket_data = {
        "asset_id": asset_id,
        "description": "Test description",
        "creator_id": user_id,
        "status": "ОТКРЫТ"
    }
    create_response = client.post("/api/v1/tickets", json=ticket_data, query_string=auth_apikey)
    ticket_id = create_response.json["id"]

    response = client.delete(f"/api/v1/tickets/{ticket_id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert "message" in response.json