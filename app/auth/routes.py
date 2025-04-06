from flask import Blueprint, request, redirect, render_template, url_for, flash, g
from flask_login import login_user, current_user, logout_user

from app.auth.forms import LoginForm
from app.users.models import User

bp = Blueprint("auth", __name__, url_prefix="/", template_folder="templates")


# @app.before_request
# def before_request():
#     g.user = current_user

@bp.route("login", methods=["GET", "POST"])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Неверный телефон или пароль", category="danger")
            # login_user(User.query.first())
        else:
            login_user(user)
            flash("Успешный вход", category="success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("index"))

    return render_template("login.html", form=form)

@bp.route("logout", methods=["GET", "POST"])
def logout():
    if current_user is not None and current_user.is_authenticated:
        logout_user()
    flash("Вы вышли", category="success")
    return redirect(url_for('main.index'))
