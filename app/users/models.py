import uuid
from enum import Enum as PyEnum

import werkzeug
from flask_login import UserMixin
from sqlalchemy import Integer, String, Column, ForeignKey, Enum, Uuid
from werkzeug.security import generate_password_hash

from app.database import model_const as mc
from app import db, login_manager


class UserStatus(PyEnum):
    ACTIVE = "ДОСТУПЕН"
    INACTIVE = "НЕ ДОСТУПЕН"


class UserModelMix(UserMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class User(db.Model, UserModelMix):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(mc.NAME_LEN), nullable=False)
    phone = Column(String(mc.PHONE_LEN), unique=True, nullable=False)
    password = Column(String(mc.SHORT_LEN), nullable=True)
    department_id = Column(ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(UserStatus), nullable=False)
    auid = Column(Uuid(), default=lambda: uuid.uuid4())

    roles = db.relationship("Role", secondary="users_roles", backref=db.backref("users", lazy="dynamic"))
    department = db.relationship("Department", back_populates="users")

    # assigned_tickets = db.relationship("Ticket", back_populates="assignee", foreign_keys="Ticket.assignee_id")

    def check_password(self, password):
        hashed_password = generate_password_hash(password)
        return self.password == hashed_password


class Department(db.Model):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(mc.NAME_LEN), nullable=False, unique=True)

    users = db.relationship("User", back_populates="department")
    # asset_options = db.relationship("AssetOption", back_populates="department")
    # tickets = db.relationship("Ticket", back_populates="department")


class Role(db.Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(mc.NAME_LEN), unique=True, nullable=False)


users_roles = db.Table(
    "users_roles",
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
