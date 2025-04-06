from flask import Blueprint
from markupsafe import escape

from app import db
from app.users.models import User

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def users_list():
    users = db.session.query(User).all()
    return "Список пользователей " + escape(str(users))
