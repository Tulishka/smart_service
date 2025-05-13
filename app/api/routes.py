from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def index():
    return {"api_version": "1.0"}
