from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    login_manager.login_message = 'Пожалуйста, войдите в систему, чтобы получить доступ к этой странице.'
    login_manager.login_message_category = 'error'
    from .main import main
    from .profile import profile
    from .Admin import Admin
    app.register_blueprint(main)
    app.register_blueprint(profile)
    app.register_blueprint(Admin)
    from .Admin.controllers import admin
    admin.init_app(app)

    login_manager.blueprint_login_views = {
        'profile': '/aut',
    }

    from .models import User, Article
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    return app
