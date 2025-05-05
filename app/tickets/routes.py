import uuid
from collections import defaultdict

from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import current_user, login_required

from app import db
from app.assets.models import Asset, AssetTypeOption
from app.tickets.forms import OptionForm
from app.tickets.models import Ticket, TicketStatus, TicketResults

bp = Blueprint('tickets', __name__, url_prefix='/tickets', template_folder="templates")


@bp.route("/", methods=["GET"])
def ticket_list():
    tickets = Ticket.query.all()
    return render_template("ticket_list.html", tickets=tickets)


@bp.route("/<int:ticket>", methods=["GET", "POST"])
def edit(ticket):
    return {}


@bp.route("/new/<asset_uid>", methods=["GET", "POST"])
@login_required
def asset_detail(asset_uid):
    asset = Asset.query.filter_by(uid=uuid.UUID(asset_uid)).one_or_none()
    if not asset:
        abort(404)
    form = OptionForm()

    already_created_options = set(
        ticket.option_id for ticket in
        Ticket.query.filter_by(asset_id=asset.id, creator_id=current_user.id, status=TicketStatus.OPENED).all()
    )

    options = [(opt.id, opt.title) for opt in asset.type.options]
    form.option.choices = options

    option_descriptions = defaultdict(str)
    for opt in form.option:
        option_obj = AssetTypeOption.query.get(int(opt.data))
        if option_obj and option_obj.description:
            option_descriptions[opt.data] = option_obj.description

    if form.validate_on_submit():
        selected_option_id = form.option.data
        option = AssetTypeOption.query.filter_by(id=selected_option_id).one_or_none()
        dep_id = option.department_id if option else None
        ticket = Ticket(
            asset_id=asset.id,
            creator_id=current_user.id,
            status=TicketStatus.OPENED,
            result=TicketResults.NEW,
            option_id=selected_option_id,
            department_id=dep_id
        )
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('tickets.asset_detail', asset_uid=asset_uid))

    return render_template(
        'asset_detail.html',
        asset=asset,
        form=form,
        option_descriptions=option_descriptions,
        already_created_options=already_created_options,
        has_options=len(already_created_options) < len(options)
    )
