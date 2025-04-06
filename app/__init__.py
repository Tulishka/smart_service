import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS", default="app.config.DevelopmentConfig"))

db = SQLAlchemy(app)
