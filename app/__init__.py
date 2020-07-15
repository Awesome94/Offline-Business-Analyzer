from flask import Flask, request, g, Blueprint, current_app
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import environ
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from config import Config


db = SQLAlchemy()
ma = Marshmallow()
login = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.DevelopmentConfig')
    Config['development'].init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    ma.init_app(app)
    login.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify 
        sslify = SSLify(app)
    return app