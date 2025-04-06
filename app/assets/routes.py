from flask import Blueprint

bp = Blueprint('assets', __name__, url_prefix='/assets')


@bp.route('/')
def index():
    return 'Главная страница Smart service!'