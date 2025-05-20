import flask_login
import pytest

URLS_CLIENT_MAPPING = (
    ("/users/", "usermanager_client"),
    ("/tickets/", "worker_client"),
    ("/reports/", "director_client"),
    ("/assets/", "asset_client")
)


@pytest.fixture
def auth_apikey(flask):
    return {'apikey': flask.config["USERS_API_KEYS"][0]}


@pytest.fixture(scope='function')
def admin_client(flask, admin_user):
    with flask.test_request_context(), flask.test_client() as _client:
        flask_login.login_user(admin_user)
        yield _client
        flask_login.logout_user()


@pytest.fixture(scope='function')
def asset_client(flask, asset_user):
    with flask.test_request_context(), flask.test_client() as _client:
        flask_login.login_user(asset_user)
        yield _client
        flask_login.logout_user()


@pytest.fixture(scope='function')
def usermanager_client(flask, usermanager_user):
    with flask.test_request_context(), flask.test_client() as _client:
        flask_login.login_user(usermanager_user)
        yield _client
        flask_login.logout_user()


@pytest.fixture(scope='function')
def director_client(flask, director_user):
    with flask.test_request_context(), flask.test_client() as _client:
        flask_login.login_user(director_user)
        yield _client
        flask_login.logout_user()


@pytest.fixture(scope='function')
def worker_client(flask, worker_user):
    with flask.test_request_context(), flask.test_client() as _client:
        flask_login.login_user(worker_user)
        yield _client
        flask_login.logout_user()


@pytest.fixture(scope='function')
def no_roles_client(flask, no_roles_user):
    with flask.test_request_context(), flask.test_client() as _client:
        flask_login.login_user(no_roles_user)
        yield _client
        flask_login.logout_user()


@pytest.fixture(params=[u for u, _ in URLS_CLIENT_MAPPING])
def web_parts_urls(request):
    return request.param
