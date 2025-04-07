from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api/v1/')


@bp.route('/')
def index():
    return {"api_version": "1.0"}
