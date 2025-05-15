import pytest

from tests.conftest import client
from tests.web.conftest import URLS_CLIENT_MAPPING


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200


def test_assets_not_logged(client, web_parts_urls):
    response = client.get(web_parts_urls, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"


@pytest.mark.parametrize("url, wl_client_n", URLS_CLIENT_MAPPING)
def test_assets_wrong_logged(wl_client_n, url, request, web_parts_urls):
    wl_client = request.getfixturevalue(wl_client_n)
    if url != web_parts_urls:
        response = wl_client.get(web_parts_urls, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/forbidden"


@pytest.mark.parametrize("url, wl_client_n", URLS_CLIENT_MAPPING)
def test_assets_properly_logged(wl_client_n, url, request):
    wl_client = request.getfixturevalue(wl_client_n)
    response = wl_client.get(url, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == url
