from app.main.routes import bp as main_bp
from app.users.routes import bp as users_bp
from app.users.users_resource import UsersResource, UsersListResource, LoginResource
from app.auth.routes import bp as auth_bp
from app.reports.routes import bp as reports_bp
from app.tickets.routes import bp as tickets_bp
from app.assets.routes import bp as assets_bp
from app.api.routes import bp as api_bp

from flask_restful import Api


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(assets_bp)
    app.register_blueprint(api_bp)


def api_setup(app):
    api = Api(app)

    api.add_resource(UsersResource, "/api/users/<int:user_id>")
    api.add_resource(UsersListResource, "/api/users")
    api.add_resource(LoginResource, "/api/login")
