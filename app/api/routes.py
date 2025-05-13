from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api/v1/')


@bp.route('/')
def index():
    """Обработчик для адреса /api/v1/"""
    return {"api_version": "1.0"}
