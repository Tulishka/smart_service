from datetime import datetime

from sqlalchemy import select, func, case, and_, between, text

from app import db
from app.assets.models import Asset, AssetType
from app.tickets.models import Ticket, TicketResults, TicketStatus
from app.users.models import User, Department


class Report:
    id: str = ""
    name: str = ""
    columns: list[str] = None
    all_reports = {}

    def __init_subclass__(cls, **kwargs):
        if cls.id:
            print("Отчет подключен", cls)
            Report.all_reports[cls.id] = cls

    def __init__(self):
        self.columns = self.columns or []

    def calculate(self, params: dict, sort_by: str = "") -> list[list[str]]:
        return []


class TicketsGroupedReport(Report):
    group_title = "---"
    group_model = User
    group_join = Ticket.assignee

    def __init__(self):
        super().__init__()
        self.columns = [
            self.group_title, "Всего заявок", "Выполнено", "Провалено", "Отменено",
            "Ср. Время (мин.)"
        ]

    def more_joins(self, query):
        return query

    def calculate(self, params: dict, sort_by: str = "") -> list[list[str]]:

        period_from = params.get("period_from")
        period_to = params.get("period_to")

        if isinstance(period_from, str):
            period_from = datetime.fromisoformat(period_from)
        if isinstance(period_to, str):
            period_to = datetime.fromisoformat(period_to)

        if db.engine.dialect.name == 'postgresql':
            time_expr = func.extract('epoch', Ticket.closed - Ticket.take_time) / 60
        else:
            # SQLite
            time_expr = (func.julianday(Ticket.closed) - func.julianday(Ticket.take_time)) * 24 * 60

        query = (
            select(
                self.group_model.name.label("0"),
                func.count(Ticket.id).label("1"),
                func.sum(case((Ticket.result == TicketResults.DONE, 1), else_=0)).label("2"),
                func.sum(case((Ticket.result == TicketResults.FAIL, 1), else_=0)).label("3"),
                func.sum(case((Ticket.result == TicketResults.CANCELED, 1), else_=0)).label("4"),
                func.round(func.avg(time_expr), 2).label("5")
            )
            .select_from(Ticket)
            .join(type(self).group_join)
        )
        query = (
            self.more_joins(query)
            .where(
                and_(
                    between(Ticket.created, period_from, period_to)
                )
            )
            .group_by(self.group_model.name)
            .order_by(text(sort_by or '"0"'))
        )
        return db.session.execute(query).all()


class WorkerTicketsReport(TicketsGroupedReport):
    id = "by_worker"
    name = "По исполнителям"
    group_title = "Исполнитель"
    group_model = User
    group_join = Ticket.assignee


class DepartmentTicketsReport(TicketsGroupedReport):
    id = "by_department"
    name = "По отделам"
    group_title = "Отдел"
    group_model = Department
    group_join = Ticket.department


class AssetTypeTicketsReport(TicketsGroupedReport):
    id = "by_asset_type"
    name = "По видам асетов"
    group_title = "Вид асета"
    group_model = AssetType
    group_join = Ticket.asset

    def more_joins(self, query):
        return super().more_joins(query).join(Asset.type)


class CreatorTicketsReport(TicketsGroupedReport):
    id = "by_creator"
    name = "По создателю"
    group_title = "Создатель"
    group_model = User
    group_join = Ticket.creator
