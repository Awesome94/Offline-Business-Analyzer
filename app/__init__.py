import boto3
from flask import Flask, request, g, Blueprint, current_app
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from itsdangerous import JSONWebSignatureSerializer as Serializer
from os import environ
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
load_dotenv(find_dotenv())
bcrypt = Bcrypt(app)

CORS(app)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
token_gen = Serializer(app.config['SECRET_KEY'])

s3 = boto3.resource('s3')
s3_path = 's3:://{name of the bucket}/{csv_name}'

db = SQLAlchemy(app)
ma = Marshmallow(app)
login = LoginManager(app)

migrate = Migrate(app, db)
manager = Manager(app)


from .api import api as api_blueprint
app.register_blueprint(api_blueprint)

from app import models