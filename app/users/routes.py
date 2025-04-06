from random import randint

from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.users.models import User, UserStatus

bp = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")

@bp.route("/", methods=["GET","POST"])
def user_list():
    if request.method == "POST":
        user = User(
            name=f"User {randint(1,100)}",
            phone=f"8{randint(1000000000,1000000000)}",
            status=UserStatus.ACTIVE,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users.user_list"))
    users = db.session.query(User).all()
    return render_template("user_list.html", users=users)
