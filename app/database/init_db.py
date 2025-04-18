from flask_sqlalchemy import SQLAlchemy

from app.users.models import User, UserStatus, Role


def create_initial_objects(db: SQLAlchemy):
    users = db.session.query(User).count()
    if users:
        return

    roles = [
        Role(name="Менеджер асетов"),
        Role(name="Исполнитель"),
        Role(name="Руководитель"),
        Role(name="Менеджер по персоналу")
    ]
    db.session.add_all(roles)

    user = User(
        phone="0",
        name="admin",
        status=UserStatus.ACTIVE,
        roles=roles
    )
    user.set_password("admin")
    db.session.add(user)

    db.session.commit()
