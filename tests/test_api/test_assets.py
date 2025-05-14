def test_create_asset(client, auth_apikey):
    asset_data = {
        "name": "Test Asset",
        "type_id": 1,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174000",
        "status": "ДОСТУПНО"
    }

    response = client.post(
        "/api/v1/assets",
        json=asset_data,
        params=auth_apikey
    )

    assert response.status_code == 200
    assert "id" in response.json


def test_get_asset(client, auth_apikey):
    asset_data = {
        "name": "Test Asset",
        "type_id": 1,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174001",
        "status": "ДОСТУПНО"
    }
    create_response = client.post("/api/v1/assets", json=asset_data, params=auth_apikey)
    asset_id = create_response.json["id"]

    response = client.get(f"/api/v1/assets/{asset_id}", params=auth_apikey)

    assert response.status_code == 200
    assert response.json["name"] == "Test Asset"


def test_update_asset(client, auth_apikey):
    asset_data = {
        "name": "Test Asset",
        "type_id": 1,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174002",
        "status": "ДОСТУПНО"
    }
    create_response = client.post("/api/v1/assets", json=asset_data, params=auth_apikey)
    asset_id = create_response.json["id"]

    update_data = {"name": "Updated Asset Name"}
    response = client.put(
        f"/api/v1/assets/{asset_id}",
        json=update_data,
        params=auth_apikey
    )

    assert response.status_code == 200
    assert response.json["name"] == "Updated Asset Name"


def test_delete_asset(client, auth_apikey):
    asset_data = {
        "name": "Test Asset",
        "type_id": 1,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174003",
        "status": "ДОСТУПНО"
    }
    create_response = client.post("/api/v1/assets", json=asset_data, params=auth_apikey)
    asset_id = create_response.json["id"]

    response = client.delete(f"/api/v1/assets/{asset_id}", params=auth_apikey)

    assert response.status_code == 200
    assert "message" in response.json
