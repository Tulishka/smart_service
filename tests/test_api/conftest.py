import os

import pytest


@pytest.fixture(scope='module')
def app():
    os.environ["APP_SETTINGS"] = "app.config.TestingConfig"
    from app import app
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_apikey(app):
    return {'apikey': app.config["USERS_API_KEYS"][0]}
