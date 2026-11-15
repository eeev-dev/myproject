from flask import Flask

from . import api_errors
from .config import Config
from .extensions import db, migrate, login_manager, bcrypt

from .models import admin as _admin_user  # регистрирует user_loader
from .routes.auth import auth
from .routes.admin import admin
from .routes.steps import steps

# API для мобильного приложения
from .routes.practice import practice
from .routes.place import place
from .routes.review import review
from .routes.student import student


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(steps)

    app.register_blueprint(practice)
    app.register_blueprint(place)
    app.register_blueprint(review)
    app.register_blueprint(student)

    api_errors.register(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Войдите, чтобы открыть кабинет'
    login_manager.login_message_category = 'warning'

    @app.context_processor
    def inject_nav():
        from flask_login import current_user
        from . import state
        if current_user.is_authenticated:
            return state.nav_context()
        return {}

    with app.app_context():
        from . import state
        state.ensure_dirs()

    return app
