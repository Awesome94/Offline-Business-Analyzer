from flask import Flask, request, g, Blueprint

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import environ

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login = LoginManager(app)


from .api import api as api_blueprint
app.register_blueprint(api_blueprint)

from app import routes, models