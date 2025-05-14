"""
Модуль, отвечающий за подключение обработчиков и API

"""

from flask_restful import Api

from app.api.assets_resource import AssetListResource, AssetTypeResource, AssetResource
from app.api.routes import bp as api_bp
from app.api.tickets_resource import TicketResource, TicketListResource
from app.api.users_resource import UsersResource, UsersListResource
from app.assets.routes import bp as assets_bp
from app.auth.routes import bp as auth_bp
from app.main.routes import bp as main_bp
from app.reports.routes import bp as reports_bp
from app.tickets.routes import bp as tickets_bp
from app.users.routes import bp as users_bp


def register_blueprints(app):
    """ Подключение обработчиков страниц

    :param app: Объект приложения
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(assets_bp)
    app.register_blueprint(api_bp)


def api_setup(app):
    """ Подключение API

    :param app: Объект приложения
    """
    api = Api(app, prefix="/api/v1/")

    api.add_resource(UsersResource, "users/<int:user_id>")
    api.add_resource(UsersListResource, "users")
    api.add_resource(AssetResource, "assets/<int:asset_id>")
    api.add_resource(AssetListResource, "assets")
    api.add_resource(AssetTypeResource, "asset_types")
    api.add_resource(TicketResource, "tickets/<int:ticket_id>")
    api.add_resource(TicketListResource, "tickets")
