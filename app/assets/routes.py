from flask import Blueprint, render_template
from app.assets.models import AssetType

bp = Blueprint("assets", __name__, url_prefix="/assets", template_folder="templates")


@bp.route("/")
def index():
    return render_template("assets_list.html")


@bp.route("/types")
def types():
    data = AssetType.query.all()
    print(data[0].image)
    return render_template("types_list.html", data=data)


@bp.route("/type_show/<int:type_id>")
def asset_type_show(type_id):
    return render_template("types_show.html", type=type_id)
