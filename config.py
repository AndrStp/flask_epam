import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Configuration class
    """
    # Flask-realted config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_very_secret_key'

    # DB credentials
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = \
        f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}