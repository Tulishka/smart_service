"""
Модуль, отвечающий за инициализацию базы данных

Происходит заполнение базы данных первоначальными данными
"""

from flask_sqlalchemy import SQLAlchemy

from app.users.models import User, UserStatus, Role, Department, Roles


def create_initial_objects(db: SQLAlchemy):
    """Функция, создающая заносящая первоначальные данные в БД

    :param db: Объект базы данных
    """

    # Если есть пользователи (а соответсвенно и данные в таблицы) - заполнять её не будем
    users = db.session.query(User).count()
    if users:
        return

    # Создание ролей
    roles = [
        Role(name=Roles.ASSET_MANAGER.value),
        Role(name=Roles.WORKER.value),
        Role(name=Roles.DIRECTOR.value),
        Role(name=Roles.USER_MANAGER.value)
    ]
    db.session.add_all(roles)

    # Создание департаментов
    deps = [
        Department(name="Техподдержка"),
        Department(name="Отдел фей вкусняшек"),
        Department(name="Отдел чистюль"),
    ]
    db.session.add_all(deps)

    # Создание админа
    user = User(
        phone="0",
        name="admin",
        status=UserStatus.ACTIVE,
        roles=roles
    )
    user.set_password("admin")
    db.session.add(user)

    db.session.commit()
