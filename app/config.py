import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY", str(uuid.uuid4()))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(basedir, 'data', 'smart_service.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
