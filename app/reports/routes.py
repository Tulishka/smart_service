from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, abort

from app.reports.report import Report
from app.users.models import Roles
from app.users.utils import role_required

bp = Blueprint("reports", __name__, url_prefix="/reports", template_folder="templates")

# Возможные периоды, для построения отчёта
PERIODS = {
    "week": (
        "за эту неделю",
        lambda end_date: (end_date - timedelta(days=end_date.weekday())).replace(hour=0, minute=0, second=0)
    ),
    "month": (
        "за этот месяц",
        lambda end_date: end_date.replace(day=1, hour=0, minute=0, second=0)
    ),
    "year": (
        "за этот год",
        lambda end_date: end_date.replace(month=1, day=1, hour=0, minute=0, second=0)
    ),
}


@bp.route("/")
@role_required(Roles.DIRECTOR)
def index():
    """обработчик, для вывода страницы отчётов

    Выводит доступные отчёты, данные для текущего отчёта.
    Так же можно выбрать период и сортировать отчёты по любой колонке как по возрастанию, так и по убыванию
    """
    report_id = request.args.get("report_id", "by_worker")
    period = request.args.get("period", "week").lower()
    if period not in PERIODS:
        period = "week"

    active_report = Report.all_reports[report_id]()

    sort_column = request.args.get("sort_column", "0")
    sort_order = request.args.get("sort_order", "a")

    if not sort_column or not sort_column.isdigit():
        sort_column = 0
    else:
        sort_column = int(sort_column)
        sort_column = min(sort_column, len(active_report.columns) - 1)

    if sort_order not in ("a", "d"):
        sort_order = "a"

    if report_id not in Report.all_reports:
        abort(404)

    period_name, get_period_from = PERIODS[period]

    period_to = datetime.now()
    period_from = get_period_from(period_to)

    report_data = active_report.calculate({
        "period_from": period_from,
        "period_to": period_to,
    },
        sort_by=f'"{sort_column}" {sort_order.replace("a", "asc").replace("d", "desc")}',
    )

    return render_template(
        "report.html",
        report_description="",
        all_reports=list(Report.all_reports.values()),
        active_report=active_report,
        report_data=report_data,
        report_id=report_id,
        period=period,
        periods=PERIODS,
        sort_column=sort_column,
        sort_order=sort_order,
        new_sort_order="d" if sort_order == "a" else "a"
    )
