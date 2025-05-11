from flask import Blueprint, render_template

from app.users.models import Roles
from app.users.utils import role_required

bp = Blueprint("reports", __name__, url_prefix="/reports", template_folder="templates")


@bp.route("/")
@role_required(Roles.DIRECTOR)
def index():
    return render_template("report_list.html")
