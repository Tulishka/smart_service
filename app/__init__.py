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
    db.create_all()

from app.modules import register_blueprints
register_blueprints(app)
