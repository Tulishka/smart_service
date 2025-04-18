from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.users.forms import UserForm
from app.users.models import User, UserStatus, Role

bp = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


@bp.route("/", methods=["GET"])
def user_list():
    users = db.session.query(User).all()
    return render_template("user_list.html", users=users)


@bp.route("/<int:user>", methods=["GET", "POST"])
def edit(user):
    user = db.get_or_404(User, user)
    all_roles = Role.query.all()

    if request.method == "GET":
        form = UserForm(
            phone=user.phone,
            name=user.name,
            status=user.status.value,
        )
        form.roles.choices = [(role.id, role.name) for role in all_roles]
        form.roles.data = [role.id for role in user.roles]
    else:
        form = UserForm()
        form.roles.choices = [(role.id, role.name) for role in all_roles]

        if form.validate_on_submit():
            user.name = form.name.data
            user.phone = form.phone.data
            user.status = UserStatus(form.status.data)

            selected_roles = Role.query.filter(Role.id.in_(form.roles.data)).all()
            user.roles = selected_roles

            db.session.add(user)
            db.session.commit()
            flash(f"Пользователь {user.name} изменен", category="info")
            return redirect(url_for("users.user_list"))

    return render_template("user_form.html", form=form)
