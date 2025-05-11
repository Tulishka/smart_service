from flask_sqlalchemy import SQLAlchemy

from app.users.models import User, UserStatus, Role, Department, Roles


def create_initial_objects(db: SQLAlchemy):
    users = db.session.query(User).count()
    if users:
        return

    roles = [
        Role(name=Roles.ASSET_MANAGER),
        Role(name=Roles.WORKER),
        Role(name=Roles.DIRECTOR),
        Role(name=Roles.USER_MANAGER)
    ]
    db.session.add_all(roles)

    deps = [
        Department(name="Техподдержка"),
        Department(name="Отдел фей вкусняшек"),
        Department(name="Отдел чистюль"),
    ]
    db.session.add_all(deps)

    user = User(
        phone="0",
        name="admin",
        status=UserStatus.ACTIVE,
        roles=roles
    )
    user.set_password("admin")
    db.session.add(user)

    db.session.commit()
