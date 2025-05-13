from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Column, ForeignKey, Enum, DateTime

from app.database import model_const as mc
from app import db


class TicketStatus(PyEnum):
    """Статусы заявки"""
    OPENED = "ОТКРЫТ"
    CLOSED = "ЗАКРЫТ"


class TicketResults(PyEnum):
    """Результаты обработки заявки"""
    NEW = "НОВЫЙ"
    IN_WORK = "В РАБОТЕ"
    DONE = "ВЫПОЛНЕНО"
    FAIL = "НЕ ВЫПОЛНЕНО"
    CANCELED = "ОТМЕНЕНО"


class Ticket(db.Model):
    """Модель заявки (тикета)"""

    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    created = Column(DateTime, default=datetime.now)  # Дата создания
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)  # Ссылка на актив
    description = Column(String(mc.DESCR_LEN))  # Описание проблемы
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Кто создал заявку
    status = Column(Enum(TicketStatus), nullable=False)  # Текущий статус
    assignee_id = Column(Integer, ForeignKey('users.id'))  # Назначенный исполнитель
    department_id = Column(Integer, ForeignKey('departments.id'))  # Отдел ответственный
    take_time = Column(DateTime)  # Время взятия в работу
    closed = Column(DateTime)  # Время закрытия
    result = Column(Enum(TicketResults))  # Результат обработки
    option_id = Column(Integer, ForeignKey('asset_type_options.id'))  # Дополнительная опция

    # Связи с другими моделями:
    asset = db.relationship("Asset", back_populates="tickets")  # Связанный актив
    creator = db.relationship("User", back_populates="created_tickets", foreign_keys=[creator_id])  # Создатель
    assignee = db.relationship("User", back_populates="assigned_tickets", foreign_keys=[assignee_id])  # Исполнитель
    department = db.relationship("Department", back_populates="tickets")  # Отдел
    comments = db.relationship("TicketComment", back_populates="ticket")  # Комментарии
    option = db.relationship("AssetTypeOption")  # Дополнительная опция

    @property
    def is_closed(self) -> bool:
        """Проверяет, закрыта ли заявка"""
        return bool(self.status == TicketStatus.CLOSED)


class TicketComment(db.Model):
    """Модель комментария к заявке"""

    __tablename__ = 'ticket_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Автор комментария
    create = Column(DateTime, nullable=False)  # Дата создания комментария
    text = Column(String(mc.DESCR_LEN), nullable=False)  # Текст комментария
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)  # Связанная заявка

    # Связи с другими моделями:
    author = db.relationship("User")  # Автор комментария
    ticket = db.relationship("Ticket", back_populates="comments")  # Заявка