from flask import Blueprint, render_template

bp = Blueprint("main", __name__, url_prefix="/", template_folder="templates")

@bp.route("/")
def index():
    return render_template("main.html")