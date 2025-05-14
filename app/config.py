"""
Модуль с конфигурацией приложения

Содержит классы:
- Config: Общий класс конфигурации
- ProductionConfig: Продакнш-конфигурация приложения
- DevelopmentConfig: Девелоп-конфигурация приложения
- TestingConfig: Тест-конфигурация приложения
"""


import json
import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Общий класс конфигурации

    Включает в себя основные настройки приложения
    """
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

    # Попытка получить ключи от API из переменных окружения
    try:
        USERS_API_KEYS = set(json.loads(os.environ.get("USERS_API_KEYS", f"['{secrets.token_urlsafe(64)}']")))
    except ValueError:
        print("USERS_API_KEYS read error")
        USERS_API_KEYS = {secrets.token_urlsafe(64)}

    # Настройки движка SQLA
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "max_overflow": 5,
        "pool_recycle": 1000,
        "pool_pre_ping": True,
    }


class ProductionConfig(Config):
    """Класс конфигурации продакш версии приложения"""
    DEBUG = False


class DevelopmentConfig(Config):
    """Класс конфигурации версии приложения для разработки"""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Класс конфигурации версии приложения для тестов"""
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
