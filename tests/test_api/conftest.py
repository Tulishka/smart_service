import pytest

API_PREFIX = "/api/v1"


@pytest.fixture
def auth_apikey(flask):
    return {'apikey': flask.config["USERS_API_KEYS"][0]}
