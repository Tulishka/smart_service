from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_user, current_user, logout_user

from app.auth.forms import LoginForm, RegisterForm
from app.users.models import User, UserStatus

from app import db

bp = Blueprint("auth", __name__, url_prefix="/", template_folder="templates")


@bp.route("login", methods=["GET", "POST"])
def login():
    redirect_url = request.args.get("next") or url_for("main.index")

    # Если пользователь уже вошел, перенаправляем далее сразу
    if current_user is not None and current_user.is_authenticated:
        return redirect(redirect_url)

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Неверный телефон или пароль", category="danger")
        else:
            login_user(user)
            flash("Успешный вход", category="success")
            return redirect(redirect_url)

    return render_template("login.html", form=form)


@bp.route("register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash("Пароли не совпадают", category="danger")
        elif User.query.filter_by(phone=form.phone.data).first():
            flash("Пользователь с таким номером уже существует", category="danger")
        else:
            user = User(
                phone=form.phone.data,
                name=form.name.data,
                status=UserStatus.ACTIVE
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Регистрация прошла успешно", category="success")

    return render_template("register.html", form=form)


@bp.route("logout", methods=["GET", "POST"])
def logout():
    if current_user is not None and current_user.is_authenticated:
        logout_user()
    flash("Вы вышли", category="success")
    return redirect(url_for('main.index'))
