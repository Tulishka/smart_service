import os


os.environ["APP_SETTINGS"] = "app.config.TestingConfig"

import uuid

import pytest

from app import app
from app.assets.models import AssetType, Asset, AssetStatus
from app.users.models import User, UserStatus, Role, Roles
from app.tickets.models import Ticket, TicketStatus, TicketResults


@pytest.fixture(scope='module')
def flask():
    yield app


@pytest.fixture
def client(flask):
    with app.app_context(), flask.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def db(flask):
    with flask.app_context():
        from app import db
        from app.database.init_db import create_initial_objects
        db.drop_all()
        db.create_all()
        create_initial_objects(db)
        yield db


@pytest.fixture
def auth_apikey(flask):
    return {'apikey': flask.config["USERS_API_KEYS"][0]}


@pytest.fixture
def admin_user(db):
    return User.query.filter_by(phone="0").first()


@pytest.fixture
def asset_user(db):
    user_roles = [Role.query.filter_by(name=Roles.ASSET_MANAGER.value).first()]
    user = User(
        name="AssetManager",
        phone="80000000001",
        status=UserStatus.ACTIVE,
        roles=user_roles,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def worker_user(db):
    user_roles = [Role.query.filter_by(name=Roles.WORKER.value).first()]
    user = User(
        name="Worker",
        phone="80000000002",
        status=UserStatus.ACTIVE,
        roles=user_roles,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def usermanager_user(db):
    user_roles = [Role.query.filter_by(name=Roles.USER_MANAGER.value).first()]
    user = User(
        name="UserManager",
        phone="80000000003",
        status=UserStatus.ACTIVE,
        roles=user_roles,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def director_user(db):
    user_roles = [Role.query.filter_by(name=Roles.DIRECTOR.value).first()]
    user = User(
        name="Director",
        phone="80000000004",
        status=UserStatus.ACTIVE,
        roles=user_roles,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def user1(db):
    user = User(
        name="user1",
        phone="81112223333",
        status=UserStatus.ACTIVE
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def asset_type1(db):
    obj = AssetType(
        name="asset_type 1",
        description="asset type description 1",
        qr_help_text="help text 1"
    )
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def asset1(db, asset_type1):
    obj = Asset(
        name="Test Asset",
        type_id=asset_type1.id,
        address="adress 1",
        uid=uuid.uuid4(),
        status=AssetStatus.ACTIVE,
    )
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def ticket1(db, asset1, user1):
    obj = Ticket(
        asset_id=asset1.id,
        creator_id=user1.id,
        status=TicketStatus.OPENED,
        result=TicketResults.NEW,
        description="Test description",
    )
    db.session.add(obj)
    db.session.commit()
    return obj
