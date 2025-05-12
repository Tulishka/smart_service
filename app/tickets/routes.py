import uuid
from collections import defaultdict
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from flask_login import current_user, login_required

from app import db
from app.assets.models import Asset, AssetTypeOption
from app.tickets.forms import OptionForm, OpenTicketForm, ClosedTicketForm
from app.tickets.models import Ticket, TicketStatus, TicketResults
from app.users.models import Department, User, Roles
from app.users.utils import role_required

bp = Blueprint('tickets', __name__, url_prefix='/tickets', template_folder="templates")


@bp.route("/", methods=["GET"])
@role_required(Roles.WORKER)
def ticket_list():
    args = request.args.to_dict()

    query = Ticket.query
    assets = list({(ticket.asset.uid, ticket.asset.name) for ticket in Ticket.query.all()})
    departments = [department.name for department in Department.query.all()]
    operators = [(operator.auid, operator.name) for operator in User.query.filter(User.roles.any(id=2)).all()]

    if "asset" in args:
        try:
            asset_uid = str(args["asset"])
            query = query.filter(Ticket.asset.has(uid=uuid.UUID(asset_uid)))
        except Exception as ex:
            flash(F"Не удалось обработать параметр асета | {ex}", category="danger")
            return redirect(url_for("tickets.ticket_list"))

    if "department" in args:
        try:
            department_id = int(args["department"])
            query = query.filter(Ticket.department_id == department_id)
        except Exception as ex:
            flash(F"Не удалось обработать параметр отдела | {ex}")
            return redirect(url_for("tickets.ticket_list"))

    if "operator" in args:
        try:
            operator_auid = args["operator"]
            query = query.filter(Ticket.assignee.has(auid=uuid.UUID(operator_auid)))
        except Exception as ex:
            flash(F"Не удалось обработать параметр исполнителя | {ex}", category="danger")
            return redirect(url_for("tickets.ticket_list"))

    if "status" in args:
        try:
            status_id = int(args["status"])

            statuses = {0: "OPENED", 1: "CLOSED"}
            status = statuses[status_id]

            query = query.filter(Ticket.status == status)
        except Exception as ex:
            flash(F"Не удалось обработать параметр статуса | {ex}", category="danger")
            return redirect(url_for("tickets.ticket_list"))

    if "result" in args:
        try:
            result_id = int(args["result"])

            results = {0: "NEW", 1: "IN_WORK", 2: "DONE", 3: "FAIL", 4: "CANCELED"}
            result = results[result_id]

            query = query.filter(Ticket.result == result)
        except Exception as ex:
            flash(F"Не удалось обработать параметр результата | {ex}", category="danger")
            return redirect(url_for("tickets.ticket_list"))

    try:
        tickets = query.all()
    except Exception as ex:
        flash(F"Не удалось осуществить запрос к БД | {ex}",
              category="danger")
        tickets = []

    return render_template("ticket_list.html",
                           tickets=tickets,
                           assets=assets,
                           departments=departments,
                           operators=operators)


@bp.route("/<int:ticket_id>", methods=["GET", "POST"])
@role_required(Roles.WORKER)
def edit(ticket_id):
    ticket = db.get_or_404(Ticket, ticket_id)
    if not ticket.is_closed or request.method == "GET":
        form = OpenTicketForm()
        form.department.choices = [(d.id, d.name) for d in Department.query.all()]
        dep = ticket.department_id
    else:
        form = ClosedTicketForm()
        dep = ticket.department.name

    if request.method == 'GET':
        form.department.data = dep
        form.status.data = ticket.status.value
        form.result.data = ticket.result.value

    if form.validate_on_submit():

        message = "Изменения сохранены", "success"
        action = form.submit.data
        if ticket.status == TicketStatus.OPENED:
            if action == "take":
                if ticket.assignee_id is None:
                    ticket.assignee_id = current_user.id
                    ticket.take_time = datetime.now()
                    message = "Вы теперь исполнитель!", "success"
                else:
                    message = "Эта заявка уже занята!", "danger"
            elif action == "release":
                if ticket.assignee_id == current_user.id:
                    ticket.assignee_id = None
                    ticket.take_time = None
                    message = "Вы отказались от заявки!", "success"
                else:
                    message = "Эта заявка итак свободна", "danger"

            ticket.result = TicketResults(form.result.data)
            ticket.department_id = form.department.data

        new_status = TicketStatus(form.status.data)

        if new_status != ticket.status:
            ticket.status = new_status
            message = f"Статус заявки изменен на '{ticket.status.value}'", "success"

            if new_status == TicketStatus.OPENED:
                ticket.closed = None
            else:
                ticket.closed = datetime.now()
                if ticket.result not in (TicketResults.CANCELED, TicketResults.DONE, TicketResults.FAIL):
                    message = (
                        f"Заявку можно закрыть только в статусах: "
                        f"{TicketResults.CANCELED.value, TicketResults.DONE.value, TicketResults.FAIL.value}",
                        "danger"
                    )

        if message[1] == "success":
            db.session.add(ticket)
            db.session.commit()

        flash(*message)
        return redirect(url_for('tickets.edit', ticket_id=ticket_id))

    if ticket.is_closed:
        form.department.render_kw = {'disabled': 'disabled'}
        form.result.render_kw = {'disabled': 'disabled'}

    return render_template("ticket_form.html",
                           ticket=ticket,
                           asset=ticket.asset,
                           form=form)


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
            description=form.description.data,
            department_id=dep_id
        )
        db.session.add(ticket)
        db.session.commit()
        flash(f"Заявка успешно создана!", "success")
        return redirect(url_for('tickets.asset_detail', asset_uid=asset_uid))

    return render_template(
        'asset_detail.html',
        asset=asset,
        form=form,
        option_descriptions=option_descriptions,
        already_created_options=already_created_options,
        has_options=len(already_created_options) < len(options)
    )
