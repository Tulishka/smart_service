from flask import Blueprint, render_template, send_from_directory

from app.config import Config

bp = Blueprint("main", __name__, url_prefix="/", template_folder="templates")


@bp.route("/")
def index():
    return render_template("main.html")


@bp.route('/media/<path:filename>')
def media_files(filename):
    return send_from_directory(Config.MEDIA_FOLDER, filename)


@bp.route("/forbidden")
def forbidden():
    return render_template("403.html")

