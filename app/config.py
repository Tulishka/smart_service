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
    APP_HOST = os.environ.get("APP_HOST", "http://127.0.0.1:5000")
    MEDIA_FOLDER = "media"
    USERS_API_KEYS = {
        "GtzUbX5Hw8diSvFS780jPnwN9tDhubMNiDo68iKJiyCT1x0GlBd3r0gyHtL8jAB",
        "CD3rlxIXQ0pGVrE72r1n33MBhH1Q5I4xd2eTgHOxBbq9HTN5BdVVZ4c3gfgNlY0"
    }


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
