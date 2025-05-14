"""
Модуль для работы с ресурсом API пользователей.

Содержит классы:
- UsersListResource: Работа с пользователями в целом (get, post запросы)
- UsersResource: Работа с отдельными пользователями по id (get, put, delete запросы)
"""

from flask import jsonify
from flask_restful import abort

from app import db
from app.api.common import BaseResource, pagination, pagination_response
from app.api.parsers.users import user_update_parser, user_parser
from app.users.models import User, Department, users_roles


def user_or_404(user_id, get_user_obj=False):
    """Функция поиска пользователя по id и возвращающая ошибку в случае неудачи

    :param user_id: Id нужного пользователя
    :param get_user_obj: Что возвращает функция (False - словарь с данными пользователя, True - объект)
    :return: (Словарь/объект пользователя)
    """
    user = User.query.get(user_id)
    if not user:
        abort(404, message=F"User {user_id} not found")
    if get_user_obj:
        return user
    return user_to_dict(user)


def abort_if_user_exists(phone):
    """Функция проверки существования пользователя с данным номером телефона

    :param phone: Номер телефона пользователя
    """
    # Возвращаем ошибку 409 (Conflict), если пользователь с таким номером уже существует
    if User.query.filter(User.phone == phone).all():
        abort(409, message="User with this phone already exists")


def user_to_dict(user):
    """Функция преобразования объекта пользователя в словарь

    :param user: Объект пользователя
    :return: Словарь с данными о пользователе
    """
    return {
        "id": user.id,
        "name": user.name,
        "department": user.department.name if user.department else "ОТСУТСТВУЕТ",
        "roles": [role.name for role in user.roles],
        "phone": user.phone,
        "status": user.status.value
    }


def set_password_or_400(user, password):
    """Функция проверки корректности длины пароля и устанавливающая его в таком случае

    :param user: Объект пользователя
    :param password: Пароль для установки
    :return: Ошибка / None
    """
    if len(password) >= 5:
        user.set_password(password)
    else:
        abort(400, message=F"the password length must be >= 5")


def put_department_or_404(user, department):
    """Функция проверки существования департамента и устанавливающаяв его в таком случае

    :param user: Объект пользователя
    :param department: Id департамента
    :return: Ошибка / None
    """
    if Department.query.get(department):
        user.department_id = department
    else:
        abort(404, message="Department with this id is not exist")


class UsersResource(BaseResource):
    """Класс для реализации работы API запросов к конкретному пользователю через его id"""

    def get(self, user_id):
        """GET-запрос для получения информации о пользователе в формате JSON

        :param user_id: Уникальный идентификтор пользователя
        :return: JSON файл с информацией о пользователе/ошибке
        """
        user = user_or_404(user_id)
        return jsonify({"users": user})

    def delete(self, user_id):
        """DELETE-запрос для удаления пользователя (Во избежание ошибок нужно использовать с осторожностью!)

        :param user_id: Уникальный идентификатор пользователя
        :return: Уведеомление об успешном удалении/ошибке
        """
        user = user_or_404(user_id, get_user_obj=True)

        users_roles.delete().where(users_roles.c.user_id == user_id)

        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "OK"})

    def put(self, user_id):
        """PUT-запрос для изменения пользователя

        :param user_id: Уникальный идентификатор пользователя
        :return: Уведомление об успешном изменении пользователя/ошибке
        """

        # Получение пользователя и аргументов, на которые есть необходимость изменить данные пользователя
        user = user_or_404(user_id, get_user_obj=True)
        args = user_update_parser.parser.parse_args()

        new_user_data = {}  # Словарь с данными, которые необходимо изменить в объекте пользователя
        for key, value in args.items():
            if value is not None:
                new_user_data[key] = value

        user.name = new_user_data.get("name", user.name)
        user.phone = new_user_data.get("phone", user.phone)

        if "phone" in new_user_data.keys():
            abort_if_user_exists(new_user_data["phone"])  # Проверка уникальности телефона

        if "department_id" in new_user_data.keys():
            put_department_or_404(user, new_user_data["department_id"])

        if "password" in new_user_data.keys():
            set_password_or_400(user, new_user_data["password"])

        db.session.commit()
        return jsonify({"success": "OK"})


class UsersListResource(BaseResource):
    """Класс для реализации общих API запросов к пользователям"""

    def get(self):
        """GET-запрос для получения информации о всех пользователях в формате JSON

        :return: JSON файл об информации о всех пользователях / ошибке
        """
        users = pagination(User.query)
        response = pagination_response(users, [user_to_dict(user) for user in users])
        return response

    def post(self):
        """POST-запрос для регистрации пользователя в системе

        :return: Id только что добавлено пользователя в случае успешного добавления / ошибку
        """

        # Получение аргументов, фигурирующих в объекте пользователя, которого нужно добавить
        args = user_parser.parser.parse_args()
        abort_if_user_exists(args["phone"])

        user = User()
        user.status = "ACTIVE"
        user.name = args["name"]
        user.phone = args["phone"]

        if args["department_id"] is not None:
            put_department_or_404(user, args["department_id"])

        set_password_or_400(user, args["password"])
        db.session.add(user)
        db.session.commit()

        return jsonify({"id": user.id})
