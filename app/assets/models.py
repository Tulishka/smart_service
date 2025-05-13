"""
Модуль с моделями базы данных, связанными с асетами.

Содержит классы:
- AssetStatus: Класс-статус для асетов
- AssetType: Модель вида асетов
- Asset: Модель самого асета
- AssetTypeOption Модель опций вида асетов
"""


from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Column, ForeignKey, Enum, Uuid

from app import db
from app.database import model_const as mc


class AssetStatus(PyEnum):
    """Класс-статус для асетов

    Содержит непосредственно статусы, которые могут быть присвоены асету
    """
    ACTIVE = "ДОСТУПНО"
    INACTIVE = "НЕ ДОСТУПНО"
    MAINTENANCE = "НА ОБСЛУЖИВАНИИ"


class AssetType(db.Model):
    """Класс-модель вида асетов

    Отвечает за создание видов асетов и взаимодействие с ними в базе данных
    """
    __tablename__ = "asset_types"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    name = Column(String(mc.NAME_LEN), nullable=False)  # Название
    description = Column(String(mc.DESCR_LEN))  # Описание
    image = Column(String(mc.URL_LEN))  # Ссылка на изображение
    qr_help_text = Column(String(mc.TITLE_LEN))  # Подпись к QR коду

    # Связи с другими моделями:
    assets = db.relationship("Asset", back_populates="type")  # Связанный актив
    options = db.relationship("AssetTypeOption", back_populates="asset_type") # Опция

    def __str__(self):
        """
        Функция, возвращающая преобразованный в строку объект вида асетов

        :return: Строковое значение названия вида асета
        """
        return f"{self.name}"


class Asset(db.Model):
    """Класс-модель асетов

    Отвечает за создание асетов и взаимодействие с ними в базе данных
    """
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    name = Column(String(mc.NAME_LEN), nullable=False, unique=True)  # Название
    type_id = Column(Integer, ForeignKey("asset_types.id", ondelete="RESTRICT"), nullable=False)  # id вида асета
    address = Column(String(mc.TITLE_LEN), nullable=False)  # Адрес асета
    uid = Column(Uuid(), nullable=False)  # UUID
    image = Column(String(mc.URL_LEN))  # Ссылка на изображение
    status = Column(Enum(AssetStatus), nullable=False)  # Статус асета
    details = Column(String(mc.DESCR_LEN))  # Детали

    # Связи с другими моделями:
    type = db.relationship("AssetType", back_populates="assets")  # Вид асета
    tickets = db.relationship("Ticket", back_populates="asset")  # Заявки

    def __str__(self):
        """
        Функция, возвращающая преобразованный в строку объект асета

        :return: Строковое значение названия асета
        """
        return f"{self.name}"


class AssetTypeOption(db.Model):
    """Класс-модель опций вида асетов

    Отвечает за создание опций вида асетов и взаимодействие с ними в базе данных
    """
    __tablename__ = "asset_type_options"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    asset_type_id = Column(Integer, ForeignKey("asset_types.id", ondelete="CASCADE"),
                           nullable=False)  # id вида асета
    title = Column(String(mc.TITLE_LEN), nullable=False)  # Заголовок
    description = Column(String(mc.DESCR_LEN), nullable=True)  # Описание
    style = Column(String(mc.NAME_LEN))  # Стиль
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"),
                           nullable=True)  # id отдела
    order = Column(Integer, nullable=False)  # Сортировка
    group = Column(Integer)  # Группа

    # Связи с другими моделями:
    asset_type = db.relationship("AssetType", back_populates="options")  # Вид асета
    department = db.relationship("Department", back_populates="asset_type_options")  # Отдел

    def __str__(self):
        """
        Функция, возвращающая преобразованный в строку объект опции

        :return: Строковое значение названия опции
        """
        return f"{self.title}"
