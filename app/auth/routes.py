from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_user

from app.auth.forms import LoginForm
from app.users.models import User

bp = Blueprint("auth", __name__, url_prefix="/", template_folder="templates")


@bp.route("login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Неверный телефон или пароль", category="danger")
        else:
            login_user(user)
            flash("Успешный вход", category="success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("index"))

    return render_template("login.html", form=form)
