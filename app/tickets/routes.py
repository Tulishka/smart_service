from flask import Blueprint, render_template

from app.tickets.models import Ticket

bp = Blueprint('tickets', __name__, url_prefix='/tickets', template_folder="templates")


@bp.route("/", methods=["GET"])
def ticket_list():
    tickets = Ticket.query.all()
    return render_template("ticket_list.html", tickets=tickets)

@bp.route("/<int:ticket>", methods=["GET", "POST"])
def edit(ticket):
    return {}