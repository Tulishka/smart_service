from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return 'Главная страница Smart service!'