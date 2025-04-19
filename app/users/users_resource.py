from flask_restful import Resource, abort
from flask import jsonify

from app.users.models import User, Role, Department
from app.users.parsers import standart_parser

from app import db


def abort_if_user_not_found(user_id):
    users = User.query.filter_by(id=user_id).first()
    if not users:
        abort(404, message=F"User {user_id} not found")


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
    pass


class UsersListResource(Resource):
    def get(self):
        users = list(map(lambda x: user_to_dict(x), User.query.all()))
        return jsonify({"users": users})

    def post(self):
        args = standart_parser.parser.parse_args()
        user = User()

        user.status = "ACTIVE"
        user.name = args["name"]
        user.phone = args["phone"]
        user.set_password(args["password"])
        db.session.add(user)
        db.session.commit()

        return jsonify({"id": user.id})
