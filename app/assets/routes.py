import json
import os

from flask import Blueprint, render_template, request, flash, url_for, redirect
from app.assets.models import AssetType, AssetTypeOption
from app.assets.forms import AssetTypeForm
from app import db
from app.users.models import Department

bp = Blueprint("assets", __name__, url_prefix="/assets", template_folder="templates")

os.makedirs("app/static/assets/uploads", exist_ok=True)
os.makedirs("app/static/assets/qr", exist_ok=True)


@bp.route("/")
def index():
    return render_template("assets_list.html")


@bp.route("/type/<int:type_id>", methods=["GET", "POST"])
def edit_type(type_id=0):
    asset_type = db.session.query(AssetType).filter_by(id=type_id).one_or_none()
    departments = [{"id": dep.id, "name": dep.name} for dep in Department.query.all()]

    if request.method == "GET":
        if asset_type:
            options = [
                {
                    'id': opt.id,
                    'title': opt.title,
                    'description': opt.description,
                    'department_id': opt.department_id,
                    'department': {'id': opt.department.id, 'name': opt.department.name} if opt.department else None
                }
                for opt in asset_type.options
            ]
            form = AssetTypeForm(
                name=asset_type.name,
                description=asset_type.description,
                image=asset_type.image
            )
        else:
            options = []
            form = AssetTypeForm()
    else:
        form = AssetTypeForm()
        if form.validate_on_submit():
            options_data = request.form.get('options_data', '[]')
            options = json.loads(options_data)

            if AssetType.query.filter((AssetType.name == form.name.data) & (AssetType.id != type_id)).first():
                form.name.errors = ("название вида асета занято",)
            else:
                file_binary = form.image.data.read()
                if not file_binary:
                    image_address = asset_type.image if asset_type else None
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
                db.session.flush()  # Чтобы получить ID для новых записей

                # Обработка опций
                current_option_ids = {opt.id for opt in asset_type.options}
                new_option_ids = set()

                for opt_data in options:
                    if str(opt_data['id']).startswith('new-'):
                        # Новая опция
                        option = AssetTypeOption(
                            asset_type_id=asset_type.id,
                            title=opt_data['title'],
                            description=opt_data['description'],
                            department_id=opt_data['department_id'] or None,
                            order=0  # Можно добавить логику для порядка
                        )
                    else:
                        # Существующая опция
                        option = AssetTypeOption.query.get(opt_data['id'])
                        if option:
                            option.title = opt_data['title']
                            option.description = opt_data['description']
                            option.department_id = opt_data['department_id'] or None

                    db.session.add(option)
                    new_option_ids.add(option.id)

                # Удаление опций, которых нет в новых данных
                for opt_id in current_option_ids - new_option_ids:
                    option = AssetTypeOption.query.get(opt_id)
                    if option:
                        db.session.delete(option)

                db.session.commit()

                flash(f"Вид асета {asset_type.name} успешно сохранён", category="info")
                return redirect(url_for("assets.types"))

    return render_template(
        "asset_type_form.html",
        form=form,
        type_id=type_id,
        options=options,
        departments=departments
    )


@bp.get("/types")
def types():
    data = AssetType.query.all()
    return render_template("types_list.html", data=data)


@bp.delete("/types/<int:type_id>")
def delete_type(type_id: int):
    atype = db.get_or_404(AssetType, type_id)
    if len(atype.assets):
        return "Нельзя удалить! Этот вид асета используется!", 400

    db.session.delete(atype)
    db.session.commit()

    return "", 204
