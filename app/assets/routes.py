from flask import Blueprint, render_template, request, flash, url_for, redirect
from app.assets.models import AssetType
from app.assets.forms import AssetTypeForm
from app import db

bp = Blueprint("assets", __name__, url_prefix="/assets", template_folder="templates")


@bp.route("/")
def index():
    return render_template("assets_list.html")


@bp.route("/types")
def types():
    data = AssetType.query.all()
    return render_template("types_list.html", data=data)


@bp.route("/type_show/<int:type_id>")
def asset_type_show(type_id):
    return render_template("types_show.html", type=type_id)


@bp.route("/add_type", methods=["GET", "POST"])
def add_type():
    form = AssetTypeForm()
    if form.validate_on_submit():
        if form.name.data.lower() in [asset_type.name.lower() for asset_type in AssetType.query.all()]:
            form.name.errors = ("Вид ассетов с таким названием уже существует",)
        else:
            file_binary = form.image.data.read()
            if not file_binary:
                image_address = "assets_standart_image.png"
            else:
                image_address = form.name.data.replace(".", "-") + ".png"
                with open("app/static/img/assets_types/" + image_address, "wb") as file:
                    file.write(file_binary)
            asset_type = AssetType(
                name=form.name.data,
                description=form.description.data,
                qr_help_text="qr_help_text",
                image=image_address
            )
            print(bool(file_binary))

            db.session.add(asset_type)
            db.session.commit()

            flash(f"Вид ассетов {asset_type.name} успешно добавлен", category="info")
            return redirect(url_for("assets.types"))

    return render_template("add_type.html", form=form)
