import pytest

from tests.conftest import client


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200


def test_assets_not_logged(client, web_parts_urls):
    response = client.get(web_parts_urls, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"


@pytest.mark.parametrize("wl_client_n, extr", (
        ("usermanager_client", "/users/"), ("worker_client", "/tickets/"),
        ("director_client", "/reports/"), ("asset_client", "/assets/")))
def test_assets_wrong_logged(wl_client_n, extr, request, web_parts_urls):
    wl_client = request.getfixturevalue(wl_client_n)
    if extr != web_parts_urls:
        response = wl_client.get(web_parts_urls, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/forbidden"


@pytest.mark.parametrize("wl_client_n, extr", (
        ("usermanager_client", "/users/"), ("worker_client", "/tickets/"),
        ("director_client", "/reports/"), ("asset_client", "/assets/")))
def test_assets_properly_logged(wl_client_n, extr, request):
    wl_client = request.getfixturevalue(wl_client_n)
    response = wl_client.get(extr, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == extr
