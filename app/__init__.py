from flask import Flask, request, g, Blueprint, current_app
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import environ
from dotenv import load_dotenv, find_dotenv
from flask_migrate import Migrate, MigrateCommand
from config import config


db = SQLAlchemy()
ma = Marshmallow()
login = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
    db.init_app(app)
    ma.init_app(app)
    login.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint,  url_prefix='/api/v1')

    return app