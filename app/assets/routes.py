import os

from flask import Blueprint, render_template, request, flash, url_for, redirect
from app.assets.models import AssetType
from app.assets.forms import AssetTypeForm
from app import db

bp = Blueprint("assets", __name__, url_prefix="/assets", template_folder="templates")

os.makedirs("app/static/assets/uploads", exist_ok=True)
os.makedirs("app/static/assets/qr", exist_ok=True)

@bp.route("/")
def index():
    return render_template("assets_list.html")


@bp.route("/type/<int:type_id>", methods=["GET", "POST"])
def edit_type(type_id=0):
    asset_type = db.session.query(AssetType).filter_by(id=type_id).one_or_none()
    if request.method == "GET":
        if asset_type:
            form = AssetTypeForm(
                name=asset_type.name,
                description=asset_type.description,
                image=asset_type.image
            )
        else:
            form = AssetTypeForm()
    else:
        form = AssetTypeForm()
        if form.validate_on_submit():
            if AssetType.query.filter((AssetType.name == form.name.data) & (AssetType.id != type_id)).first():
                form.name.errors = ("название вида асета занято",)
            else:
                file_binary = form.image.data.read()
                if not file_binary:
                    image_address = None
                else:
                    image_address = form.name.data.replace(".", "-") + ".png"
                    with open("app/static/assets/uploads/" + image_address, "wb") as file:
                        file.write(file_binary)
                if not asset_type:
                    asset_type = AssetType()
                asset_type.name = form.name.data
                asset_type.description = form.description.data
                asset_type.qr_help_text = "qr_help_text"
                if image_address:
                    asset_type.image = image_address

                db.session.add(asset_type)
                db.session.commit()

                flash(f"Вид асета {asset_type.name} успешно сохранён", category="info")
                return redirect(url_for("assets.types"))

    return render_template("asset_type_form.html", form=form)


@bp.route("/types")
def types():
    data = AssetType.query.all()
    return render_template("types_list.html", data=data)
