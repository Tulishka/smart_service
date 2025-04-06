from flask_login import UserMixin
from sqlalchemy import Integer, String, Column, ForeignKey

from app import db


class UserModelMix(UserMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class User(db.Model, UserModelMix):
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(255))

    roles = db.relationship("Role", secondary="user_role", backref=db.backref("users", lazy="dynamic"))


class Role(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)


user_role = db.Table(
    "user_role",
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True)
)
