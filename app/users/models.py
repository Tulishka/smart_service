import uuid
from enum import Enum as PyEnum

import werkzeug
from flask_login import UserMixin
from sqlalchemy import Integer, String, Column, ForeignKey, Enum, Uuid
from werkzeug.security import generate_password_hash

from app.database import model_const as mc
from app import db, login_manager


class Roles(PyEnum):
    """Роли пользователей в системе"""
    USER_MANAGER = "Менеджер по персоналу"
    ASSET_MANAGER = "Менеджер асетов"
    WORKER = "Исполнитель"
    DIRECTOR = "Руководитель"


class UserStatus(PyEnum):
    """Статусы активности пользователя"""
    ACTIVE = "ДОСТУПЕН"
    INACTIVE = "НЕ ДОСТУПЕН"


class UserModelMix(UserMixin):
    """Миксин для добавления методов Flask-Login"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class User(db.Model, UserModelMix):
    """Модель пользователя системы"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    name = Column(String(mc.NAME_LEN), nullable=False)  # Имя пользователя
    phone = Column(String(mc.PHONE_LEN), unique=True, nullable=False)  # Телефон
    hashed_password = Column(String(mc.URL_LEN), nullable=True)  # Хеш пароля
    department_id = Column(ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)  # Отдел
    status = Column(Enum(UserStatus), nullable=False)  # Статус активности
    auid = Column(Uuid(), default=lambda: uuid.uuid4())  # Альтернативный UUID

    # Связи:
    roles = db.relationship("Role", secondary="users_roles", backref=db.backref("users", lazy="joined"), lazy="joined")
    department = db.relationship("Department", back_populates="users")

    assigned_tickets = db.relationship("Ticket", back_populates="assignee", foreign_keys="Ticket.assignee_id")
    created_tickets = db.relationship("Ticket", back_populates="creator", foreign_keys="Ticket.creator_id")

    def check_password(self, password):
        """Проверяет соответствие пароля хешу

        :param password: Пароль для проверки
        :returns: True если пароль верный, иначе False
        """
        return werkzeug.security.check_password_hash(self.hashed_password, password)

    def set_password(self, password):
        """Устанавливает новый пароль пользователю

        :param password: Новый пароль
        """
        self.hashed_password = generate_password_hash(password)

    def role_names(self):
        """Возвращает строку с названиями ролей пользователя

        :returns: Строка с перечислением ролей через запятую
        """
        return ", ".join(role.name for role in self.roles)

    def has_role(self, role: Roles) -> bool:
        """Проверяет наличие конкретной роли у пользователя

        :param role: Роль для проверки
        :returns: True если роль есть, иначе False
        """
        return role.value in (role.name for role in self.roles)

    @property
    def has_asset_access(self) -> bool:
        """Проверяет доступ к управлению активами"""
        return self.has_role(Roles.ASSET_MANAGER)

    @property
    def has_ticket_access(self) -> bool:
        """Проверяет доступ к работе с заявками"""
        return self.has_role(Roles.WORKER)

    @property
    def has_user_access(self) -> bool:
        """Проверяет доступ к управлению пользователями"""
        return self.has_role(Roles.USER_MANAGER)

    @property
    def has_director_access(self) -> bool:
        """Проверяет наличие прав руководителя"""
        return self.has_role(Roles.DIRECTOR)

    def __str__(self):
        return f"{self.name}"


class Department(db.Model):
    """Модель отдела"""

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    name = Column(String(mc.NAME_LEN), nullable=False, unique=True)  # Название отдела

    # Связи:
    users = db.relationship("User", back_populates="department")
    asset_type_options = db.relationship("AssetTypeOption", back_populates="department")
    tickets = db.relationship("Ticket", back_populates="department")

    def __str__(self):
        return f"{self.name}"


class Role(db.Model):
    """Модель роли пользователя"""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    name = Column(String(mc.NAME_LEN), unique=True, nullable=False)  # Название роли

    def __str__(self):
        return f"{self.name}"


users_roles = db.Table(
    "users_roles",
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)


@login_manager.user_loader
def load_user(user_id):
    """Загрузчик пользователя для Flask-Login

    :param user_id: ID пользователя
    :returns: Объект пользователя или None
    """
    return User.query.filter_by(id=user_id).first()
