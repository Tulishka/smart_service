from app.assets.models import Asset
from tests.test_api.conftest import API_PREFIX


def test_create_asset(client, auth_apikey, asset_type1):
    asset_data = {
        "name": "Test Asset",
        "type_id": asset_type1.id,
        "address": "Test Address",
        "uid": "123e4567-e89b-12d3-a456-426614174000",
        "status": "ДОСТУПНО"
    }

    response = client.post(
        f"{API_PREFIX}/assets",
        json=asset_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert "id" in response.json


def test_get_asset(client, auth_apikey, asset1):

    response = client.get(f"{API_PREFIX}/assets/{asset1.id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert response.json["id"] == asset1.id
    assert response.json["name"] == asset1.name


def test_update_asset(client, auth_apikey, asset1):

    update_data = {"name": "Updated Asset Name"}
    response = client.put(
        f"{API_PREFIX}/assets/{asset1.id}",
        json=update_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert response.json["name"] == "Updated Asset Name"


def test_delete_asset(client, auth_apikey, asset1, db):

    response = client.delete(f"{API_PREFIX}/assets/{asset1.id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert "message" in response.json
    assert Asset.query.filter_by(id=asset1.id).one_or_none() is None