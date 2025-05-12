from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, abort

from app.reports.report import WorkerTicketsReport, DepartmentTicketsReport
from app.users.models import Roles
from app.users.utils import role_required

bp = Blueprint("reports", __name__, url_prefix="/reports", template_folder="templates")

all_reports = {
    "by_worker": WorkerTicketsReport(),
    "by_department": DepartmentTicketsReport()
}


@bp.route("/")
@role_required(Roles.DIRECTOR)
def index():
    report_id = request.args.get("report_id", "by_worker")
    if report_id not in all_reports:
        abort(404)

    active_report = all_reports[report_id]

    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    period_from = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    report_data = active_report.calculate({
        "period_from": period_from,
        "period_to": now,
    })

    return render_template(
        "report.html",
        report_description="* Данные выведены за текущую неделю",
        all_reports=list(all_reports.values()),
        active_report=active_report,
        report_data=report_data
    )
