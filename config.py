from os import environ


class Config:
    """Base configuration class"""

    # Flask-realted config
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV', 'development')
    SECRET_KEY = environ.get('SECRET_KEY', 'my_very_secret_key')

    # DB credentials
    DB_USER = environ.get('DB_USER')
    DB_PASSWORD = environ.get('DB_PASSWORD')
    DB_HOST = environ.get('DB_HOST')
    DB_PORT = environ.get('DB_PORT')
    DB_NAME = environ.get('DB_NAME')

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = \
        f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MAIL
    MAIL_SERVER=environ.get('MAIL_SERVER')
    MAIL_PORT=environ.get('MAIL_PORT')
    MAIL_USE_TLS=environ.get('MAIL_USE_TLS')
    MAIL_USERNAME=environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=environ.get('MAIL_PASSWORD')

    # MISCELLANEOUS
    FLASK_MAIL_SUBJECT_PREFIX=environ.get('FLASK_MAIL_SUBJECT_PREFIX')