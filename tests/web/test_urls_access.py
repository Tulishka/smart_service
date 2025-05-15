import pytest

from tests.conftest import client
from tests.web.conftest import URLS_CLIENT_MAPPING


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200


def test_access_to_urls_when_user_not_logged(client, web_parts_urls):
    response = client.get(web_parts_urls, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"


def test_access_to_urls_when_logged_user_with_no_roles(no_roles_client, web_parts_urls):
    response = no_roles_client.get(web_parts_urls, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/forbidden"


@pytest.mark.parametrize("url, wl_client_n", URLS_CLIENT_MAPPING)
def test_access_to_urls_logged_user_with_wrong_role(wl_client_n, url, request, web_parts_urls):
    wl_client = request.getfixturevalue(wl_client_n)
    if url != web_parts_urls:
        response = wl_client.get(web_parts_urls, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/forbidden"


@pytest.mark.parametrize("url, wl_client_n", URLS_CLIENT_MAPPING)
def test_access_to_urls_logged_user_with_right_role(wl_client_n, url, request):
    wl_client = request.getfixturevalue(wl_client_n)
    response = wl_client.get(url, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == url
