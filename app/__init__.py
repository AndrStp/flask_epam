from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'
migrate = Migrate()
mail = Mail()


def create_app():
    """Factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db, directory='app/migrations')
    from .models.user import User
    
    login_manager.init_app(app)
    mail.init_app(app)

    # TODO Blueprints
    # main blueprint
    from app.main import main
    app.register_blueprint(main, url_prefix='/')

    # auth blueprint
    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # api blueprint
    from app.rest import api
    app.register_blueprint(api, url_prefix='/api')

    return app
