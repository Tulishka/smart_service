from flask_restful import Resource, abort
from flask import jsonify

from app.users.models import User, Role, Department, users_roles
from app.users.parsers import standart_parser, unrequired_parser, login_parser

from flask_login import current_user, login_user

from app import db


def abort_if_user_not_found(user_id):
    users = User.query.filter_by(id=user_id).first()
    if not users:
        abort(404, message=F"User {user_id} not found")


def abort_if_no_access():
    if not current_user.is_authenticated:
        abort(403, message=F"Access allowed only for registered users")
    else:  # Здесь будем сверять роль пользователя с той, что будет иметь доступ к этому API
        pass


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


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_no_access()
        abort_if_user_not_found(user_id)
        user = user_to_dict(User.query.get(user_id))
        return jsonify({"users": user})

    def delete(self, user_id):
        abort_if_no_access()
        abort_if_user_not_found(user_id)
        user = User.query.get(user_id)

        users_roles.delete().where(users_roles.c.user_id == user_id)

        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "OK"})


class UsersListResource(Resource):
    def get(self):
        abort_if_no_access()
        users = list(map(lambda x: user_to_dict(x), User.query.all()))
        return jsonify({"users": users})

    def post(self):
        abort_if_no_access()
        args = standart_parser.parser.parse_args()
        user = User()

        user.status = "ACTIVE"
        user.name = args["name"]
        user.phone = args["phone"]
        user.set_password(args["password"])
        db.session.add(user)
        db.session.commit()

        return jsonify({"id": user.id})


class LoginResource(Resource):
    def post(self):
        args = login_parser.parser.parse_args()
        user = User.query.filter_by(phone=args["phone"]).first()
        if not user or not user.check_password(args["password"]):
            abort("404", message="incorrect phone or password")
        else:
            login_user(user)
            return jsonify({"success": "OK"})
