from conftest import Ticket, TicketStatus
from tests.test_api.conftest import API_PREFIX


def test_create_ticket(client, auth_apikey, user1, asset1):

    ticket_data = {
        "asset_id": asset1.id,
        "description": "Test description",
        "creator_id": user1.id,
        "status": TicketStatus.OPENED.value
    }

    response = client.post(
        f"{API_PREFIX}/tickets",
        json=ticket_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert "id" in response.json


def test_get_ticket(client, auth_apikey, ticket1):
    response = client.get(f"{API_PREFIX}/tickets/{ticket1.id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert response.json["description"] == "Test description"


def test_update_ticket(client, auth_apikey, asset1, ticket1):

    update_data = {"status": "ЗАКРЫТ"}
    response = client.put(
        f"{API_PREFIX}/tickets/{ticket1.id}",
        json=update_data,
        query_string=auth_apikey
    )

    assert response.status_code == 200
    assert response.json["status"] == "ЗАКРЫТ"


def test_delete_ticket(client, auth_apikey, ticket1, db):

    assert Ticket.query.filter_by(id=ticket1.id).one_or_none() is not None

    response = client.delete(f"{API_PREFIX}/tickets/{ticket1.id}", query_string=auth_apikey)

    assert response.status_code == 200
    assert "message" in response.json
    assert Ticket.query.filter_by(id=ticket1.id).one_or_none() is None
