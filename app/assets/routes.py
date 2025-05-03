import json
import os
import uuid

from flask import Blueprint, render_template, request, flash, url_for, redirect
from markupsafe import Markup

from app import db
from app.config import Config
from app.assets.forms import AssetTypeForm, AssetForm
from app.assets.models import AssetType, AssetTypeOption, Asset, AssetStatus
from app.core import utils
from app.users.models import Department
from app.assets.qr import create_qr_if_need

bp = Blueprint("assets", __name__, url_prefix="/assets", template_folder="templates")

os.makedirs("app/static/assets/uploads", exist_ok=True)
os.makedirs("app/static/assets/qr", exist_ok=True)


@bp.route("/")
def index():
    assets = Asset.query.all()
    return render_template("assets_list.html", assets=assets)


@bp.route("/codes")
def codes():
    error_message = ""
    try:
        args = request.args.to_dict()["assets"]
        assets_ids = [int(i) for i in args.split(",")]

        assets = db.session.query(Asset).filter(Asset.id.in_(assets_ids)).all()
        assets_data = [
            {
                "id": str(asset.id),
                "uid": str(asset.uid),
                "name": asset.name,
                "qr_help_text": asset.type.qr_help_text,
            }
            for asset in assets
        ]

        if not assets_data:
            error_message = F"По данным id ничего не найдено."

    except Exception as ex:
        error_message = F"Ошибка при получении QR-кодов: {type(ex)}. Проверьте корректность запроса."
        assets_data = []

    return render_template("codes_list.html", assets_data=assets_data, error_message=error_message)


@bp.route("/codes_process", methods=["POST"])
def codes_process():
    selected_ids = ",".join(request.form.getlist('checkboxes'))
    return redirect(url_for("assets.codes", assets=selected_ids))


@bp.route("/type/<int:type_id>", methods=["GET", "POST"])
def edit_type(type_id=0):
    asset_type = db.session.query(AssetType).filter_by(id=type_id).one_or_none()
    departments = [{"id": dep.id, "name": dep.name} for dep in Department.query.all()]
    options = []

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
                qr_help_text=asset_type.qr_help_text,
                image=asset_type.image
            )
        else:
            form = AssetTypeForm()
    else:
        form = AssetTypeForm()
        if form.validate_on_submit():
            options_data = request.form.get('options_data', '[]')
            options = json.loads(options_data)

            if AssetType.query.filter((AssetType.name == form.name.data) & (AssetType.id != type_id)).first():
                form.name.errors = ("название вида асета занято",)
            else:
                if not asset_type:
                    asset_type = AssetType()

                if form.image.data:
                    image_address = utils.save_upload_file("assets", form.image.data)
                else:
                    image_address = asset_type.image if asset_type else None

                asset_type.name = form.name.data
                asset_type.description = form.description.data
                asset_type.qr_help_text = form.qr_help_text.data
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


@bp.route("/<int:asset_id>", methods=["GET", "POST"])
def edit(asset_id=0, type_id=0):
    asset = Asset.query.filter_by(id=asset_id).one_or_none()
    types = AssetType.query.all()
    type_id = type_id or request.args.get("type_id")

    if request.method == "GET":
        if asset:
            form = AssetForm(
                name=asset.name,
                type_id=asset.type_id,
                address=asset.address,
                image=asset.image,
                status=asset.status.value,
                details=asset.details,
            )
        else:
            form = AssetForm(type_id=type_id)

        form.type_id.choices = [(type.id, type.name) for type in types]
    else:
        form = AssetForm()
        form.type_id.choices = [(type.id, type.name) for type in types]
        if form.validate_on_submit():
            if Asset.query.filter((Asset.name == form.name.data) & (Asset.id != asset_id)).first():
                form.name.errors = ("название асета занято",)
            else:
                if not asset:
                    asset = Asset()
                    asset.uid = uuid.uuid4()

                if not form.image.data:
                    image_address = asset.image if asset else None
                else:
                    image_address = utils.save_upload_file("assets", form.image.data)

                asset.name = form.name.data
                asset.type_id = form.type_id.data
                asset.address = form.address.data
                asset.image = image_address
                asset.status = AssetStatus(form.status.data)
                asset.details = form.details.data

                db.session.add(asset)
                db.session.commit()

                result = create_qr_if_need(asset.uid)
                if result:
                    html_link = (F"<a href='{Config.APP_HOST}/assets/codes?assets={asset.id}' class='alert-link'>"
                                 F"Перейти на страницу печати QR-кода.</a>")
                else:
                    html_link = ''
                flash(Markup(f"Асет {asset.name} сохранён. {html_link}"), category="info")

                if type_id:
                    return redirect(url_for("assets.types"))
                return redirect(url_for("assets.index"))

    return render_template("asset_form.html", form=form)
