from datetime import datetime

from sqlalchemy import select, func, case, and_, between, text

from app import db
from app.assets.models import Asset, AssetType
from app.tickets.models import Ticket, TicketResults
from app.users.models import User, Department


class Report:
    """Базовый класс для генерации отчетов"""

    id: str = ""  # Идентификатор отчета
    name: str = ""  # Название отчета
    columns: list[str] = None  # Список колонок отчета
    all_reports = {}  # Словарь всех доступных отчетов

    def __init_subclass__(cls, **kwargs):
        """Автоматически регистрирует подклассы отчетов при их определении"""
        if cls.id:
            print("Отчет подключен", cls)
            Report.all_reports[cls.id] = cls

    def __init__(self):
        """Инициализирует отчет с пустыми колонками или переопределенными в подклассе"""
        self.columns = self.columns or []

    def calculate(self, params: dict, sort_by: str = "") -> list[list[str]]:
        """Вычисляет данные отчета.

        :param params: Параметры для формирования отчета
        :param sort_by: Поле для сортировки результатов

        :return: cписок строк с данными отчета
        """
        return []


class TicketsGroupedReport(Report):
    """Базовый класс для отчетов по заявкам с группировкой"""

    group_title = "---"  # Заголовок группы
    group_model = User  # Модель для группировки
    group_join = Ticket.assignee  # Поле для соединения с Ticket

    def __init__(self):
        """Инициализирует отчет с колонками по умолчанию"""
        super().__init__()
        self.columns = [
            self.group_title, "Всего заявок", "Выполнено", "Провалено", "Отменено",
            "Ср. Время (мин.)"
        ]

    def more_joins(self, query):
        """Добавляет дополнительные join к запросу.

        :param query: Query
        :return: Модифицированный запрос - Query
        """
        return query

    def calculate(self, params: dict, sort_by: str = "") -> list[list[str]]:
        """Вычисляет данные отчета с группировкой.

        :param params: Словарь параметров (должен содержать period_from и period_to)
        :param sort_by: Поле для сортировки результатов
        :return: Список строк с данными отчета
        """
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
    """Отчет по заявкам с группировкой по исполнителям"""

    id = "by_worker"
    name = "По исполнителям"
    group_title = "Исполнитель"
    group_model = User
    group_join = Ticket.assignee


class DepartmentTicketsReport(TicketsGroupedReport):
    """Отчет по заявкам с группировкой по отделам"""

    id = "by_department"
    name = "По отделам"
    group_title = "Отдел"
    group_model = Department
    group_join = Ticket.department


class AssetTypeTicketsReport(TicketsGroupedReport):
    """Отчет по заявкам с группировкой по видам асетов"""

    id = "by_asset_type"
    name = "По видам асетов"
    group_title = "Вид асета"
    group_model = AssetType
    group_join = Ticket.asset

    def more_joins(self, query):
        """Добавляет соединение с типом актива"""
        return super().more_joins(query).join(Asset.type)


class CreatorTicketsReport(TicketsGroupedReport):
    """Отчет по заявкам с группировкой по создателям"""

    id = "by_creator"
    name = "По создателю"
    group_title = "Создатель"
    group_model = User
    group_join = Ticket.creator
