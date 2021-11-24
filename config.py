import os


class Config:
    """
    Configuration class
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_very_secret_key'

