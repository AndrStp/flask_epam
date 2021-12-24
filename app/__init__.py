import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from app_config import app_config
from logging_config import logging_config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'
migrate = Migrate()
mail = Mail()


def create_app(config_name: str='default') -> Flask:
    """Factory pattern"""
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    migrate.init_app(app, db, directory='app/migrations')
    from .models.user import User
    from .models.course import Course
    
    login_manager.init_app(app)
    mail.init_app(app)

    #logging
    logging.config.dictConfig(logging_config)

    from app.main import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.rest import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app
