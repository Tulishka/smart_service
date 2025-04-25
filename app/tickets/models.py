from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Column, ForeignKey, Enum, DateTime

from app.database import model_const as mc
from app import db

from sqlalchemy import Column


class TicketStatus(PyEnum):
    OPENED = "ОТКРЫТ"
    CLOSED = "ЗАКРЫТ"


class TicketResults(PyEnum):
    NEW = "НОВЫЙ"
    IN_WORK = "В РАБОТЕ"
    DONE = "ВЫПОЛНЕНО"
    FAIL = "НЕ ВЫПОЛНЕНО"
    CANCELED = "ОТМЕНЕНО"


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, nullable=False)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    description = Column(String(mc.DESCR_LEN))
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(TicketStatus), nullable=False)
    assignee_id = Column(Integer, ForeignKey('users.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))
    take_time = Column(DateTime)
    closed = Column(DateTime)
    result = Column(Enum(TicketResults))
    option_id = Column(Integer, ForeignKey('asset_type_options.id'))

    asset = db.relationship("Asset", back_populates="tickets")
    creator = db.relationship("User", back_populates="created_tickets", foreign_keys=[creator_id])
    assignee = db.relationship("User", back_populates="assigned_tickets", foreign_keys=[assignee_id])
    department = db.relationship("Department", back_populates="tickets")
    comments = db.relationship("TicketComment", back_populates="ticket")
    option = db.relationship("AssetTypeOption")


class TicketComment(db.Model):
    __tablename__ = 'ticket_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    create = Column(DateTime, nullable=False)
    text = Column(String(mc.DESCR_LEN), nullable=False)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)

    author = db.relationship("User")
    ticket = db.relationship("Ticket", back_populates="comments")
