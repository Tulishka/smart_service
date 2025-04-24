from flask import Blueprint, render_template

bp = Blueprint("assets", __name__, url_prefix="/assets", template_folder="templates")


@bp.route("/")
def index():
    return render_template("assets_list.html")


@bp.route("/types")
def types():
    return render_template("types_list.html")
