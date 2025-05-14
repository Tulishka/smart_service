import os
import sys

import pytest
from flask import Flask
from sqlalchemy import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_sqlalchemy import SQLAlchemy
from app.modules import api_setup


@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config.from_object("app.config.TestingConfig")

    db = SQLAlchemy(app)

    api_setup(app)

    with app.app_context():
        from app.database import all_models
        from app.database.init_db import create_initial_objects

        db.create_all()

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        raise Exception(str(tables))
        create_initial_objects(db)



@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_apikey(app):
    return {'apikey': app.config["USERS_API_KEYS"]}