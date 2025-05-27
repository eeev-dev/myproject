from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .extensions import db, migrate, login_manager

from .routes.user import user
from .routes.post import post
from .routes.intern import intern
from .routes.home import main
from .routes.place import place
from .routes.review import review

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(intern)
    app.register_blueprint(main)
    app.register_blueprint(place)
    app.register_blueprint(review)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Вы не можете получить доступ к данной странице. Нужно сначала войти'

    with app.app_context():
        db.create_all()

    return app
