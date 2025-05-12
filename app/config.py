import json
import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(64))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(basedir, 'data', 'smart_service.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_HOST = os.environ.get("APP_HOST", "http://127.0.0.1:5000")
    MEDIA_FOLDER = "media"
    try:
        USERS_API_KEYS = set(json.loads(os.environ.get("USERS_API_KEYS", f"['{secrets.token_urlsafe(64)}']")))
    except ValueError:
        print("USERS_API_KEYS read error")
        USERS_API_KEYS = {secrets.token_urlsafe(64)}


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
