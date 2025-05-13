import uuid
from collections import defaultdict
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from flask_login import current_user, login_required

from app import db
from app.assets.models import Asset, AssetTypeOption
from app.core.filter_utils import apply_filter
from app.tickets.forms import OptionForm, OpenTicketForm, ClosedTicketForm
from app.tickets.models import Ticket, TicketStatus, TicketResults
from app.users.models import Department, User, Roles
from app.users.utils import role_required

bp = Blueprint('tickets', __name__, url_prefix='/tickets', template_folder="templates")

TICKET_FILTERS = {
    "asset": lambda value: Ticket.asset.has(uid=uuid.UUID(value)),
    "department": lambda value: Ticket.department_id == int(value),
    "operator": lambda value: Ticket.assignee.has(auid=uuid.UUID(value)),
    "status": lambda value: Ticket.status == ["OPENED", "CLOSED"][int(value)],
    "result": lambda value: Ticket.result == ["NEW", "IN_WORK", "DONE", "FAIL", "CANCELED"][int(value)],
}


@bp.route("/", methods=["GET"])
@role_required(Roles.WORKER)
def ticket_list():
    """Отображает список заявок с возможностью фильтрации

    :returns: Страница со списком заявок
    """
    args = request.args.to_dict()

    query = Ticket.query
    assets = list({(ticket.asset.uid, ticket.asset.name) for ticket in Ticket.query.all()})
    departments = [(department.id, department.name) for department in Department.query.all()]
    operators = [(operator.auid, operator.name) for operator in User.query.all()]

    tickets = []
    try:
        tickets = apply_filter(query, TICKET_FILTERS, args).all()
    except ValueError as ex:
        flash(str(ex), "danger")
    except Exception:
        flash(F"Не удалось осуществить запрос к БД", "danger")

    return render_template(
        "ticket_list.html",
        tickets=tickets,
        assets=assets,
        departments=departments,
        operators=operators
    )


@bp.route("/<int:ticket_id>", methods=["GET", "POST"])
@role_required(Roles.WORKER)
def edit(ticket_id):
    """Редактирование заявки

    :param ticket_id: ID заявки
    :returns: Страница редактирования заявки или редирект
    """
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
    """Создание новой заявки

    :param asset_uid: UID асета
    :returns: страница создания заявки или редирект
    """
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
