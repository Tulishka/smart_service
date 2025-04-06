from flask_login import UserMixin
from sqlalchemy import Integer, String, Column, ForeignKey

from app import db


class UserModelMix(UserMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class User(db.Model, UserModelMix):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True)
    password = Column(String(255))
    department_id = Column(ForeignKey("departments.id", ondelete="SET NULL"))
    status = Column(Integer, nullable=False)

    roles = db.relationship("Role", secondary="users_roles", backref=db.backref("users", lazy="dynamic"))
    department = db.relationship("Department", back_populates="users")
    assigned_tickets = db.relationship("Ticket", back_populates="assignee", foreign_keys="Ticket.assignee_id")



class Department(db.Model):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    users = db.relationship("User", back_populates="department")
    asset_options = db.relationship("AssetOption", back_populates="department")
    tickets = db.relationship("Ticket", back_populates="department")


class Role(db.Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    user_roles = db.relationship("UserRole", back_populates="role")


users_roles = db.Table(
    "users_roles",
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)
