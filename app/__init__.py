import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS", default="app.config.DevelopmentConfig"))

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Требуется выполнить вход"
login_manager.login_message_category = "info"

with app.app_context():
    from app.database import all_models
    from app.database.init_db import create_initial_objects

    db.create_all()
    create_initial_objects(db)

from app.modules import register_blueprints
from app.modules import api_setup

register_blueprints(app)
api_setup(app)
