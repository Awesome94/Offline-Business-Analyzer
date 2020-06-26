import boto3
from flask import Flask, request, g, Blueprint, current_app
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
token_gen = Serializer(app.config['SECRET_KEY'], app.config['TOKEN_EXPIRATION'])

s3 = boto3.resource('s3')
s3_path = 's3:://{name of the bucket}/{csv_name}'

db = SQLAlchemy(app)
ma = Marshmallow(app)
login = LoginManager(app)


from .api import api as api_blueprint
app.register_blueprint(api_blueprint)

from app import models