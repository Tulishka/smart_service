from flask_restful import Resource, abort
from flask import jsonify, request

from app.users.models import User, Role, Department, users_roles
from app.users.parsers import standart_parser, unrequired_parser, login_parser

from functools import wraps

from flask_login import current_user, login_user

from app import db

from app.config import Config


def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        apikey = request.args.get('apikey')
        if not apikey:
            abort(401, message="API key is missing")
        if apikey not in Config.USERS_API_KEYS:
            abort(403, message="Invalid API key")
        return f(*args, **kwargs)
    return decorated


def user_or_404(user_id, get_user_obj=False):
    user = User.query.get(user_id)
    if not user:
        abort(404, message=F"User {user_id} not found")
    if get_user_obj:
        return user
    return user_to_dict(user)


def abort_if_user_exists(phone):
    if User.query.filter(User.phone == phone).all():
        abort(409, message="User with this phone already exists")


def user_to_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "department": Department.query.filter_by(id=user.department_id).first().name if user.department_id is not None
        else "ОТСУТСТВУЕТ",
        "roles": [role.name for role in user.roles],
        "phone": user.phone,
        "status": "ДОСТУПЕН" if user.status.name == "ACTIVE" else "НЕ ДОСТУПЕН"
    }


def set_password_or_400(user, password):
    if len(password) >= 5:
        user.set_password(password)
    else:
        abort(400, message=F"the password length must be >= 5")


class UsersResource(Resource):
    @api_key_required
    def get(self, user_id):
        user = user_or_404(user_id)
        return jsonify({"users": user})

    @api_key_required
    def delete(self, user_id):
        user = user_or_404(user_id, get_user_obj=True)

        users_roles.delete().where(users_roles.c.user_id == user_id)

        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "OK"})

    @api_key_required
    def put(self, user_id):
        user = user_or_404(user_id, get_user_obj=True)
        args = unrequired_parser.parser.parse_args()

        new_user_data = {}
        for key, value in args.items():
            if value is not None:
                new_user_data[key] = value

        user.name = new_user_data.get("name", user.name)
        user.phone = new_user_data.get("phone", user.phone)

        if "phone" in new_user_data.keys():
            abort_if_user_exists(new_user_data["phone"])

        if "department_id" in new_user_data.keys():
            if Department.query.get(new_user_data["department_id"]):
                user.department_id = new_user_data["department_id"]

        if "password" in new_user_data.keys():
            set_password_or_400(user, new_user_data["password"])
        db.session.commit()
        return jsonify({"success": "OK"})


class UsersListResource(Resource):
    @api_key_required
    def get(self):
        users = list(map(lambda x: user_to_dict(x), User.query.all()))
        return jsonify({"users": users})

    @api_key_required
    def post(self):
        args = standart_parser.parser.parse_args()
        abort_if_user_exists(args["phone"])

        user = User()

        user.status = "ACTIVE"
        user.name = args["name"]
        user.phone = args["phone"]
        set_password_or_400(user, args["password"])
        db.session.add(user)
        db.session.commit()

        return jsonify({"id": user.id})
