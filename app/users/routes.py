from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.users.forms import UserForm, DepartmentForm
from app.users.models import User, UserStatus, Role, Department, Roles
from app.users.utils import role_required

bp = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


@bp.route("/", methods=["GET"])
@role_required(Roles.USER_MANAGER)
def user_list():
    users = db.session.query(User).all()
    return render_template("user_list.html", users=users)


@bp.route("/<int:user>", methods=["GET", "POST"])
@role_required(Roles.USER_MANAGER)
def edit(user):
    user = db.get_or_404(User, user)
    all_roles = Role.query.all()

    if request.method == "GET":
        form = UserForm(
            phone=user.phone,
            name=user.name,
            status=user.status.value,
        )
        form.department.data = user.department_id
    else:
        form = UserForm()

    form.roles.choices = [(role.id, role.name) for role in all_roles]
    form.department.choices = [(0, "(НЕ НАЗНАЧЕН)")] + [(d.id, d.name) for d in Department.query.all()]

    if form.validate_on_submit():
        if User.query.filter((User.phone == form.phone.data) & (User.id != user.id)).first():
            form.phone.errors = ("Пользователь с таким номером уже существует",)
        else:
            user.name = form.name.data
            user.phone = form.phone.data
            if form.department.data:
                user.department_id = form.department.data
            else:
                user.department_id = None
            user.status = UserStatus(form.status.data)

            selected_roles = Role.query.filter(Role.id.in_(form.roles.data)).all()
            user.roles = selected_roles

            db.session.add(user)
            db.session.commit()
            flash(f"Пользователь {user.name} изменен", category="info")
            return redirect(url_for("users.user_list"))

    form.roles.data = [role.id for role in user.roles]
    return render_template("user_form.html", form=form)


@bp.route("/departments", methods=["GET"])
@role_required(Roles.USER_MANAGER)
def department_list():
    departments = db.session.query(Department).all()
    return render_template("department_list.html", departments=departments)


@bp.route("/departments/<int:department_id>", methods=["GET", "POST"])
@role_required(Roles.USER_MANAGER)
def department(department_id=0):
    department = Department.query.filter_by(id=department_id).one_or_none()
    if not department:
        department = Department()
    if request.method == "GET":
        form = DepartmentForm(
            name=department.name,
        )
    else:
        form = DepartmentForm()
        if form.validate_on_submit():
            if User.query.filter((Department.name == form.name.data) & (Department.id != department.id)).first():
                form.name.errors = ("Отдел с таким названием уже существует",)
            else:
                department.name = form.name.data
                db.session.add(department)
                db.session.commit()
                flash(f"Отдел {department.name} сохранён", category="info")
                return redirect(url_for("users.department_list"))

    return render_template("department_form.html", form=form, department_id=department_id)


@bp.delete("/departments/<int:department_id>")
@role_required(Roles.USER_MANAGER)
def delete_department(department_id: int):
    dep = db.get_or_404(Department, department_id)
    if len(dep.users) or len(dep.asset_type_options) or len(dep.tickets):
        return "Нельзя удалить! Этот отдел используется!", 400
    db.session.delete(dep)
    db.session.commit()

    return "", 204
