from random import randint

from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.users.models import User, UserStatus

bp = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


@bp.route("/", methods=["GET"])
def user_list():
    users = db.session.query(User).all()
    return render_template("user_list.html", users=users)
