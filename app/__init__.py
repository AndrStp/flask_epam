from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)
# db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
app.config.from_object(Config)


from app.views import routes

