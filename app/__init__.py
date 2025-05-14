"""
Модуль с инициализацией приложения

"""


import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()  # Чтение переменных окружения из .env
app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS", default="app.config.DevelopmentConfig"))

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Требуется выполнить вход"
login_manager.login_message_category = "info"

# Инициализация базы данных, занесение в случае необходимсоти перовначальных данных
with app.app_context():
    from app.database import all_models
    from app.database.init_db import create_initial_objects

    db.create_all()
    create_initial_objects(db)

from app.modules import register_blueprints
from app.modules import api_setup

# Установвка обработчиков и API
register_blueprints(app)
api_setup(app)
