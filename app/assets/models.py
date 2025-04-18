from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Column, ForeignKey, Enum, Uuid

from app.database import model_const as mc
from app import db


class AssetStatus(PyEnum):
    ACTIVE = "ДОСТУПНО"
    INACTIVE = "НЕ ДОСТУПНО"
    MAINTENANCE = "НА ОБСЛУЖИВАНИИ"


class AssetType(db.Model):
    __tablename__ = "asset_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(mc.NAME_LEN), nullable=False)
    description = Column(String(mc.DESCR_LEN))
    image = Column(String(mc.URL_LEN))
    qr_help_text = Column(String(mc.TITLE_LEN))

    assets = db.relationship("Asset", back_populates="type")
    options = db.relationship("AssetTypeOption", back_populates="asset_type")


class Asset(db.Model):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(mc.NAME_LEN), nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey("asset_types.id"), nullable=False)
    address = Column(String(mc.TITLE_LEN), nullable=False)
    uid = Column(Uuid(), nullable=False)
    image = Column(String(mc.URL_LEN))
    status = Column(Enum(AssetStatus), nullable=False)
    details = Column(String(mc.DESCR_LEN))

    type = db.relationship("AssetType", back_populates="assets")
    tickets = db.relationship("Ticket", back_populates="asset")


class AssetOption(db.Model):
    __tablename__ = "asset_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(mc.TITLE_LEN), nullable=False)
    description = Column(String(mc.DESCR_LEN))
    style = Column(String(mc.NAME_LEN))
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    department = db.relationship("Department")
    types = db.relationship("AssetTypeOption", back_populates="asset_option")


class AssetTypeOption(db.Model):
    __tablename__ = "asset_type_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_type_id = Column(Integer, ForeignKey("asset_types.id", ondelete="CASCADE"), nullable=False)
    asset_option_id = Column(Integer, ForeignKey("asset_options.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, nullable=False)
    group = Column(Integer)

    asset_type = db.relationship("AssetType", back_populates="options")
    asset_option = db.relationship("AssetOption", back_populates="types")
