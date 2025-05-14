from flask import request, jsonify, current_app
from flask_restful import Resource, reqparse, abort
from sqlalchemy.orm import Query, QueryPropertyDescriptor

from app import db
from functools import wraps

from app.config import Config

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', location='args', type=int, default=1, help='Номер страницы')
pagination_parser.add_argument('per_page', location='args', type=int, default=50, help='Элементов на страницу')


def api_key_required(f):
    """Декоратор для проверки корректности ключа API

    :param f: Входящая функция
    :return: Результат функции после проверки ключа API
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        apikey = request.args.get('apikey')
        # Случай отсутствия ключа API в query параметрах
        if not apikey:
            abort(401, message="API key is missing")

        # Случай передачи неверного ключа API в параметрах
        if apikey not in current_app.config["USERS_API_KEYS"]:
            abort(403, message="Invalid API key")
        return f(*args, **kwargs)

    return decorated


def handle_db_errors(f):
    """Декоратор для обработки ошибок БД"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

    return wrapper


class BaseResource(Resource):
    method_decorators = [api_key_required]


def pagination(query):
    """Общий метод для пагинации возвращаемого запроса"""
    args = pagination_parser.parse_args()
    page = args['page']
    per_page = args['per_page']
    return query.paginate(page=page, per_page=per_page, error_out=False)


def pagination_response(paginated_query, items: list, items_name: str = "items"):
    return jsonify({
        items_name: items,
        'total': paginated_query.total,
        'pages': paginated_query.pages,
        'current_page': paginated_query.page
    })
